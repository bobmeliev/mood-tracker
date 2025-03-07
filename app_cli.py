import sqlite3
import datetime
import time

# Database setup
def init_db():
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp INTEGER,
        time_of_day TEXT,
        mood INTEGER,
        sleep_quality INTEGER,
        wake_up_time TEXT,
        bedtime TEXT,
        thoughts TEXT,
        gratitude TEXT
    )''')
    conn.commit()
    conn.close()

# Input validation functions
def get_valid_int(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_valid_time(prompt):
    while True:
        time_input = input(prompt)
        try:
            datetime.datetime.strptime(time_input, "%H:%M")
            return time_input
        except ValueError:
            print("Invalid time format. Please enter in HH:MM (24-hour format).")

def get_text_input(prompt):
    print(prompt + " (Type 'END' on a new line to finish)")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()

def get_gratitude_entries():
    gratitude_entries = []
    while True:
        gratitude = get_text_input("Enter a gratitude:")
        if gratitude:
            gratitude_entries.append(gratitude)
        more = input("Would you like to add another gratitude? (yes/no): ").strip().lower()
        if more != "yes":
            break
    return gratitude_entries

# Collect user journal entry
def collect_entry():
    print("Choose time of day: Morning, Afternoon, Evening")
    time_of_day = input("Enter your choice: ").strip().lower()
    
    if time_of_day not in ["morning", "afternoon", "evening"]:
        print("Invalid choice. Please choose Morning, Afternoon, or Evening.")
        return
    
    timestamp = int(time.time())
    mood = None
    sleep_quality = None
    wake_up_time = None
    bedtime = None
    thoughts = ""
    gratitude_entries = []
    
    if time_of_day == "morning":
        mood = get_valid_int("Morning mood (1-10): ", 1, 10)
        sleep_quality = get_valid_int("Sleep quality (1-10): ", 1, 10)
        wake_up_time = get_valid_time("Wake up time (HH:MM): ")
        gratitude_entries = get_gratitude_entries()
        thoughts = get_text_input("Morning thoughts: ")
    
    elif time_of_day == "afternoon":
        mood = get_valid_int("Afternoon mood (1-10): ", 1, 10)
    
    elif time_of_day == "evening":
        mood = get_valid_int("Evening mood (1-10): ", 1, 10)
        bedtime = get_valid_time("What time are you going to bed (HH:MM)?: ")
        thoughts = get_text_input("Evening thoughts: ")
    
    gratitude_text = ", ".join(gratitude_entries) if gratitude_entries else None
    
    save_to_db(timestamp, time_of_day, mood, sleep_quality, wake_up_time, bedtime, thoughts, gratitude_text)
    print("Journal entry saved successfully!")

# Save data to database
def save_to_db(timestamp, time_of_day, mood, sleep_quality, wake_up_time, bedtime, thoughts, gratitude):
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO journal (timestamp, time_of_day, mood, sleep_quality, wake_up_time, bedtime, thoughts, gratitude)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (timestamp, time_of_day, mood, sleep_quality, wake_up_time, bedtime, thoughts, gratitude))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    collect_entry()
