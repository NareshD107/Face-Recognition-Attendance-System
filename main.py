import os
import sys
import shutil
import cv2
from datetime import datetime

# Configuration
DATASET_DIR = "dataset"
ATTENDANCE_FILE = "attendance/attendance.csv"

def main_menu():
    while True:
        print("\n" + "="*45)
        print("   FACE RECOGNITION ATTENDANCE SYSTEM   ")
        print("="*45)
        print(" 1. Capture New Faces")
        print(" 2. Generate Face Encodings")
        print(" 3. Start Attendance System")
        print(" 4. View Attendance Logs")
        print(" 5. Register New Student")
        print(" 6. View Registered Students")
        print(" 7. Update Student Details")
        print(" 8. Delete Student Data")
        print(" 9. Export Attendance Report")
        print("10. Search Attendance by Date")
        print("11. Real-time Attendance Summary")
        print("12. Clear Attendance Logs")
        print("13. Check Camera Connection")
        print("14. Exit")
        print("-" * 45)
        
        choice = input("Enter your choice (1-14): ").strip()

        if choice == '1' or choice == '5':
            print(f"\n[INFO] Starting {'Registration' if choice == '5' else 'Capture'} Module...")
            os.system(f'"{sys.executable}" capture_faces.py')
        
        elif choice == '2':
            print("\n[INFO] Starting Face Encoding Module...")
            os.system(f'"{sys.executable}" encode_faces.py')
        
        elif choice == '3':
            print("\n[INFO] Starting Live Attendance System...")
            os.system(f'"{sys.executable}" attendance.py')
            
        elif choice == '4':
            display_logs()
            
        elif choice == '6':
            view_students()
            
        elif choice == '7':
            update_student()
            
        elif choice == '8':
            delete_student()
            
        elif choice == '9':
            export_report()
            
        elif choice == '10':
            search_by_date()
            
        elif choice == '11':
            attendance_summary()
            
        elif choice == '12':
            clear_logs()
            
        elif choice == '13':
            check_camera()
            
        elif choice == '14':
            print("[INFO] Exiting... Goodbye!")
            sys.exit()
            
        else:
            print("[ERROR] Invalid choice. Please try again.")

# --- Helper Functions ---

def display_logs():
    if not os.path.exists(ATTENDANCE_FILE):
        print("\n[ERROR] No attendance logs found yet.")
        return

    print("\n" + "-"*45)
    print(f"{'Name':<20} | {'Date':<12} | {'Time':<10}")
    print("-" * 45)
    
    try:
        with open(ATTENDANCE_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]: # Skip header
                parts = line.strip().split(',')
                if len(parts) == 3:
                    name, date, time = parts
                    print(f"{name:<20} | {date:<12} | {time:<10}")
    except Exception as e:
        print(f"[ERROR] Could not read logs: {e}")
    print("-" * 45)

def view_students():
    print("\n[INFO] Registered Students:")
    if not os.path.exists(DATASET_DIR):
        print("None (Dataset directory not found)")
        return
    
    students = [d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))]
    if not students:
        print("None (No folders found in dataset)")
    else:
        for i, student in enumerate(students, 1):
            print(f"{i}. {student.replace('_', ' ')}")

def update_student():
    view_students()
    old_name = input("\nEnter the name of student to update (as shown above): ").strip().replace(" ", "_")
    old_path = os.path.join(DATASET_DIR, old_name)
    
    if os.path.exists(old_path):
        new_name = input("Enter the new name: ").strip().replace(" ", "_")
        new_path = os.path.join(DATASET_DIR, new_name)
        try:
            os.rename(old_path, new_path)
            print(f"[SUCCESS] Updated {old_name} to {new_name}")
            print("[INFO] Please run 'Generate Face Encodings' to apply changes.")
        except Exception as e:
            print(f"[ERROR] Could rename: {e}")
    else:
        print("[ERROR] Student folder not found.")

def delete_student():
    view_students()
    name = input("\nEnter name of student to DELETE: ").strip().replace(" ", "_")
    path = os.path.join(DATASET_DIR, name)
    
    if os.path.exists(path):
        confirm = input(f"Are you sure you want to delete ALL data for {name}? (y/n): ").lower()
        if confirm == 'y':
            try:
                shutil.rmtree(path)
                print(f"[SUCCESS] Deleted {name} and all their images.")
                print("[INFO] Please run 'Generate Face Encodings' to update the model.")
            except Exception as e:
                print(f"[ERROR] Could not delete: {e}")
    else:
        print("[ERROR] Student not found.")

def export_report():
    if not os.path.exists(ATTENDANCE_FILE):
        print("[ERROR] No logs to export.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_name = f"attendance_report_{timestamp}.csv"
    try:
        shutil.copy(ATTENDANCE_FILE, export_name)
        print(f"[SUCCESS] Report exported as: {os.path.abspath(export_name)}")
    except Exception as e:
        print(f"[ERROR] Export failed: {e}")

def search_by_date():
    date_to_find = input("Enter date to search (YYYY-MM-DD): ").strip()
    if not os.path.exists(ATTENDANCE_FILE):
        print("[ERROR] No logs found.")
        return

    found = False
    print("\n" + "-"*45)
    print(f"{'Name':<20} | {'Date':<12} | {'Time':<10}")
    print("-" * 45)
    
    with open(ATTENDANCE_FILE, 'r') as f:
        for line in f.readlines()[1:]:
            if date_to_find in line:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    name, date, time = parts
                    print(f"{name:<20} | {date:<12} | {time:<10}")
                    found = True
    
    if not found:
        print("No records found for that date.")
    print("-" * 45)

def attendance_summary():
    today = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(ATTENDANCE_FILE):
        print("[INFO] No attendance data available.")
        return

    attendees = set()
    with open(ATTENDANCE_FILE, 'r') as f:
        for line in f.readlines()[1:]:
            parts = line.strip().split(',')
            if len(parts) == 3 and parts[1] == today:
                attendees.add(parts[0])
    
    print("\n" + "="*45)
    print(f" ATTENDANCE SUMMARY FOR TODAY ({today}) ")
    print("="*45)
    print(f"Total Students Recognized: {len(attendees)}")
    if attendees:
        print("List: " + ", ".join([a.replace('_', ' ') for a in attendees]))
    print("-" * 45)

def clear_logs():
    confirm = input("Are you sure you want to CLEAR ALL attendance logs? (y/n): ").lower()
    if confirm == 'y':
        try:
            with open(ATTENDANCE_FILE, 'w') as f:
                f.write("Name,Date,Time\n")
            print("[SUCCESS] All logs have been cleared.")
        except Exception as e:
            print(f"[ERROR] Could not clear logs: {e}")

def check_camera():
    print("[INFO] Checking camera connection... Press 'q' to close the test window.")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open camera. Please check your hardware.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Camera connected but failed to return frames.")
            break
        
        cv2.putText(frame, "Camera OK - Press 'q' to exit", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Camera Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Camera check completed.")

if __name__ == "__main__":
    main_menu()
