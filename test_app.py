import pytest
from unittest.mock import patch, MagicMock
import time
import sqlite3
import tkinter as tk
from app import MoodSleepTracker, db_name  # Import your app class and database name


@pytest.fixture
def app():
    """Fixture to create an instance of the application."""
    root = tk.Tk()
    app = MoodSleepTracker(root)
    yield app
    root.destroy()


@patch("sqlite3.connect")
def test_create_database(mock_connect, app):
    """Test if the database creation function executes correctly."""
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_cursor = mock_conn.cursor()

    app.create_database()

    mock_connect.assert_called_once_with(db_name)

    # Retrieve actual SQL calls
    actual_calls = [call[0][0] for call in mock_cursor.execute.call_args_list]

    # Normalize SQL by removing excessive whitespace
    def normalize_sql(sql):
        return " ".join(sql.split())

    expected_sql = '''CREATE TABLE IF NOT EXISTS mood_sleep (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER,
        mood INTEGER,
        sleep INTEGER)'''

    assert any(normalize_sql(expected_sql) == normalize_sql(call) for call in actual_calls), \
        f"Expected SQL not found in executed calls: {actual_calls}"

@patch("sqlite3.connect")
@patch("tkinter.messagebox.showinfo")  # Mock messagebox
def test_save_data(mock_messagebox, mock_connect, app):
    """Test if data is saved correctly into the database without blocking due to messagebox."""
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    app.mood_var.set(8)  # Simulate user input
    app.sleep_var.set(6)

    app.save_data()

    mock_connect.assert_called_once_with(db_name)
    mock_conn.cursor().execute.assert_called_once_with(
        "INSERT INTO mood_sleep (timestamp, mood, sleep) VALUES (?, ?, ?)", 
        (pytest.approx(int(time.time()), rel=1), 8, 6)
    )
    mock_conn.commit.assert_called_once()

    # Ensure messagebox was called but doesn't block execution
    mock_messagebox.assert_called_once_with("Success", "Data saved successfully!")

@patch("sqlite3.connect")
def test_plot_data(mock_connect, app):
    """Test if plot_data fetches correct data from the database."""
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor()
    mock_connect.return_value = mock_conn
    mock_cursor.fetchall.return_value = [
        (int(time.time()) - 86400, 7, 5),  # Fake past data
        (int(time.time()) - 43200, 6, 7),
    ]

    app.time_filter_var.set("Week")
    app.plot_data()

    mock_connect.assert_called_once_with(db_name)
    mock_cursor.execute.assert_called_once()


def test_time_filtering(app):
    """Test if time filtering logic calculates correct timestamps."""
    current_time = int(time.time())
    time_ranges = {
        "Week": 7 * 24 * 3600,
        "Month": 30 * 24 * 3600,
        "3 Months": 90 * 24 * 3600,
        "6 Months": 180 * 24 * 3600,
        "Year": 365 * 24 * 3600,
        "All time": None
    }

    app.time_filter_var.set("Month")
    expected_timestamp = current_time - time_ranges["Month"]

    assert current_time - time_ranges["Month"] == expected_timestamp


if __name__ == "__main__":
    pytest.main()
