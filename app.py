import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as tb

db_name = "mood_sleep_tracker.db"

class MoodSleepTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood & Sleep Tracker v1")
        self.root.geometry("900x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Apply dark theme
        self.style = tb.Style("darkly")

        # Database setup
        self.create_database()

        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create Data Tab
        self.create_data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.create_data_frame, text="Create Data")
        self.setup_create_tab()

        # View Data Tab
        self.view_data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_data_frame, text="View Data")
        self.setup_view_tab()

        # Exit button
        self.exit_button = ttk.Button(self.main_frame, text="Exit", command=self.on_closing)
        self.exit_button.pack(side=tk.RIGHT, padx=5, pady=5, anchor='e')

    def create_database(self):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS mood_sleep (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          timestamp INTEGER,
                          mood INTEGER,
                          sleep INTEGER)''')
        conn.commit()
        conn.close()

    def setup_create_tab(self):
        ttk.Label(self.create_data_frame, text="Mood (1-10):", font=("Arial", 12)).pack(pady=5)
        self.mood_var = tk.IntVar(value=5)
        self.mood_dropdown = ttk.Combobox(self.create_data_frame, textvariable=self.mood_var, values=list(range(1, 11)), state="readonly")
        self.mood_dropdown.pack(pady=5)

        ttk.Label(self.create_data_frame, text="Sleep Quality (1-10):", font=("Arial", 12)).pack(pady=5)
        self.sleep_var = tk.IntVar(value=5)
        self.sleep_dropdown = ttk.Combobox(self.create_data_frame, textvariable=self.sleep_var, values=list(range(1, 11)), state="readonly")
        self.sleep_dropdown.pack(pady=5)

        self.save_button = ttk.Button(self.create_data_frame, text="Save Data", command=self.save_data)
        self.save_button.pack(pady=20)

    def save_data(self):
        mood = self.mood_var.get()
        sleep = self.sleep_var.get()
        timestamp = int(time.time())  # Store as UNIX epoch

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mood_sleep (timestamp, mood, sleep) VALUES (?, ?, ?)", (timestamp, mood, sleep))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data saved successfully!")

    def setup_view_tab(self):
        control_frame = ttk.Frame(self.view_data_frame)
        control_frame.pack(pady=5)

        # Dropdown for filtering time range
        self.time_filter_var = tk.StringVar(value="Week")
        ttk.Label(control_frame, text="Last:").pack(side=tk.LEFT, padx=5)
        self.time_filter_dropdown = ttk.Combobox(control_frame, textvariable=self.time_filter_var, 
                                                 values=["Week", "Month", "3 Months", "6 Months", "Year", "All time"],
                                                 state="readonly")
        self.time_filter_dropdown.pack(side=tk.LEFT, padx=5)
        self.time_filter_dropdown.bind("<<ComboboxSelected>>", lambda event: self.plot_data())

        # Checkboxes for showing mood and sleep quality
        self.show_mood_var = tk.BooleanVar(value=True)
        self.show_sleep_var = tk.BooleanVar(value=True)
        
        self.mood_checkbox = ttk.Checkbutton(control_frame, text="Show Mood", variable=self.show_mood_var, command=self.plot_data)
        self.mood_checkbox.pack(side=tk.LEFT, padx=5)
        self.sleep_checkbox = ttk.Checkbutton(control_frame, text="Show Sleep Quality", variable=self.show_sleep_var, command=self.plot_data)
        self.sleep_checkbox.pack(side=tk.LEFT, padx=5)

        self.graph_frame = ttk.Frame(self.view_data_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        self.plot_data()

    def plot_data(self):
        time_filter = self.time_filter_var.get()
        current_time = int(time.time())
        time_ranges = {
            "Week": 7 * 24 * 3600,
            "Month": 30 * 24 * 3600,
            "3 Months": 90 * 24 * 3600,
            "6 Months": 180 * 24 * 3600,
            "Year": 365 * 24 * 3600,
            "All time": None
        }

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if time_ranges[time_filter] is not None:
            cursor.execute("SELECT timestamp, mood, sleep FROM mood_sleep WHERE timestamp >= ? ORDER BY timestamp", 
                           (current_time - time_ranges[time_filter],))
        else:
            cursor.execute("SELECT timestamp, mood, sleep FROM mood_sleep ORDER BY timestamp")
        data = cursor.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("No Data", "No data available to display.")
            return

        timestamps = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row[0])) for row in data]
        mood_scores = [row[1] for row in data]
        sleep_scores = [row[2] for row in data]

        # Clear previous graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4))
        if self.show_mood_var.get():
            ax.plot(timestamps, mood_scores, marker='o', label='Mood', linestyle='-', color='cyan')
        if self.show_sleep_var.get():
            ax.plot(timestamps, sleep_scores, marker='s', label='Sleep Quality', linestyle='-', color='magenta')
        
        ax.set_xticks(timestamps)
        ax.set_xticklabels(timestamps, rotation=45, ha='right', fontsize=8)
        ax.set_ylabel("Score (1-10)")
        ax.set_title("Mood & Sleep Quality Over Time")
        ax.legend()
        ax.grid()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_closing(self):
        self.root.destroy()
        exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodSleepTracker(root)
    root.mainloop()
