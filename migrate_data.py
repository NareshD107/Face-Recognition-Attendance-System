import csv
import os
import database
from datetime import datetime

def migrate_csv_to_db():
    attendance_file = "attendance/attendance.csv"
    if not os.path.exists(attendance_file):
        print("[INFO] No legacy attendance.csv found. Skipping migration.")
        return

    print("[INFO] Starting migration from CSV to SQLite...")
    database.init_db()
    
    count = 0
    try:
        with open(attendance_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader) # Skip header
            
            for row in reader:
                if len(row) == 3:
                    name, date, time = row
                    # Register student if not exists
                    database.add_student(name)
                    # Log attendance (as a general entry without session)
                    if database.log_attendance(name):
                        count += 1
                        
        print(f"[SUCCESS] Migrated {count} new records from CSV to Database.")
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")

if __name__ == "__main__":
    migrate_csv_to_db()
