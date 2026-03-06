import sqlite3
import os
from datetime import datetime

DB_NAME = "attendance.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            email TEXT,
            roll_number TEXT,
            department TEXT,
            phone_number TEXT,
            registration_date TEXT NOT NULL
        )
    ''')
    
    # Sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL
        )
    ''')
    
    # Attendance logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            session_id INTEGER,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[INFO] Database initialized.")

def add_student(name, email=None, roll_number=None, department=None, phone_number=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO students (name, email, roll_number, department, phone_number, registration_date) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, roll_number, department, phone_number, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
    except sqlite3.Error as e:
        print(f"[ERROR] DB: {e}")
    finally:
        conn.close()

def create_session(subject_name):
    conn = get_connection()
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    cursor.execute("INSERT INTO sessions (subject_name, date, start_time) VALUES (?, ?, ?)", 
                   (subject_name, date, time))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def log_attendance(name, session_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")
    
    # Check if already marked for this session or today (if no session)
    if session_id:
        cursor.execute("SELECT id FROM attendance_logs WHERE student_name = ? AND session_id = ?", (name, session_id))
    else:
        cursor.execute("SELECT id FROM attendance_logs WHERE student_name = ? AND date = ? AND session_id IS NULL", (name, date_str))
        
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO attendance_logs (student_name, session_id, date, time) VALUES (?, ?, ?, ?)", 
                       (name, session_id, date_str, time_str))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students")
    students = [row[0] for row in cursor.fetchall()]
    conn.close()
    return students

def get_logs_by_date(date_to_find=None):
    conn = get_connection()
    cursor = conn.cursor()
    if date_to_find:
        cursor.execute("""
            SELECT student_name, attendance_logs.date, attendance_logs.time, subject_name 
            FROM attendance_logs 
            LEFT JOIN sessions ON attendance_logs.session_id = sessions.id
            WHERE attendance_logs.date = ?
            ORDER BY attendance_logs.date DESC, attendance_logs.time DESC
        """, (date_to_find,))
    else:
        cursor.execute("""
            SELECT student_name, attendance_logs.date, attendance_logs.time, subject_name 
            FROM attendance_logs 
            LEFT JOIN sessions ON attendance_logs.session_id = sessions.id
            ORDER BY attendance_logs.date DESC, attendance_logs.time DESC
        """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_today_summary():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT student_name FROM attendance_logs WHERE date = ?", (today,))
    attendees = [row[0] for row in cursor.fetchall()]
    conn.close()
    return attendees

def get_all_students_full():
    """Returns list of tuples with all student details."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, roll_number, department, email FROM students ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_student_name(old_name, new_name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE students SET name = ? WHERE name = ?", (new_name, old_name))
        cursor.execute("UPDATE attendance_logs SET student_name = ? WHERE student_name = ?", (new_name, old_name))
        conn.commit()
    except sqlite3.Error as e:
        print(f"[ERROR] DB Update: {e}")
    finally:
        conn.close()

def delete_student(name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE name = ?", (name,))
        cursor.execute("DELETE FROM attendance_logs WHERE student_name = ?", (name,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"[ERROR] DB Delete: {e}")
    finally:
        conn.close()

def get_attendance_trends():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, COUNT(DISTINCT student_name) 
        FROM attendance_logs 
        GROUP BY date 
        ORDER BY date ASC 
        LIMIT 7
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def get_top_attendees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT student_name, COUNT(*) as count 
        FROM attendance_logs 
        GROUP BY student_name 
        ORDER BY count DESC 
        LIMIT 5
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def get_department_distribution():
    """Returns count of students per department."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT department, COUNT(*) FROM students GROUP BY department")
    data = cursor.fetchall()
    conn.close()
    return data

def get_attendance_by_department():
    """Returns attendance counts grouped by department."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.department, COUNT(al.id) 
        FROM attendance_logs al
        JOIN students s ON al.student_name = s.name
        GROUP BY s.department
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def get_student_email(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM students WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def clear_all_logs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance_logs")
    cursor.execute("DELETE FROM sessions")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
