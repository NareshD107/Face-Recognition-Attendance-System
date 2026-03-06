import os
import sys
import shutil
import cv2
import database
from datetime import datetime

# Configuration
DATASET_DIR = "dataset"
ATTENDANCE_FILE = "attendance/attendance.csv" # Keep for backward compatibility/export

# Initialize DB on start
database.init_db()

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
            subject = input("\nEnter Subject/Session Name (e.g., Math, OS): ").strip()
            if not subject:
                subject = "General"
            session_id = database.create_session(subject)
            print(f"\n[INFO] Starting Live Attendance for {subject} (Session ID: {session_id})...")
            os.system(f'"{sys.executable}" attendance.py --session {session_id}')
            
        elif choice == '4':
            display_logs_db()
            
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

def display_logs_db():
    print("\n--- View Attendance Logs ---")
    print("1. View Today's Logs")
    print("2. View Logs for a Specific Date")
    print("3. View All Logs (History)")
    sub_choice = input("Enter choice (1-3): ").strip()

    if sub_choice == '1':
        date_to_find = datetime.now().strftime("%Y-%m-%d")
    elif sub_choice == '2':
        date_to_find = input("Enter date (YYYY-MM-DD): ").strip()
    elif sub_choice == '3':
        date_to_find = None
    else:
        print("[ERROR] Invalid choice.")
        return
        
    logs = database.get_logs_by_date(date_to_find)
    if not logs:
        print(f"\n[INFO] No logs found.")
        return

    print("\n" + "="*70)
    print(f"{'Student Name':<20} | {'Date':<12} | {'Time':<10} | {'Subject/Session':<15}")
    print("=" * 70)
    for name, date, time, subject in logs:
        sub = subject if subject else "General/Legacy"
        print(f"{name:<20} | {date:<12} | {time:<10} | {sub:<15}")
    print("=" * 70)

def view_students():
    print("\n[INFO] Registered Students:")
    students_fs = [d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))] if os.path.exists(DATASET_DIR) else []
    students_db = database.get_all_students()
    
    # Combine or show from DB primarily
    all_students = sorted(list(set(students_fs + students_db)))
    
    if not all_students:
        print("None (No data found)")
    else:
        for i, student in enumerate(all_students, 1):
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
            database.update_student_name(old_name, new_name)
            print(f"[SUCCESS] Updated {old_name} to {new_name}")
            print("[INFO] Please run 'Generate Face Encodings' to apply changes.")
        except Exception as e:
            print(f"[ERROR] Could not rename: {e}")
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
                database.delete_student(name)
                print(f"[SUCCESS] Deleted {name} and all their images.")
                print("[INFO] Please run 'Generate Face Encodings' to update the model.")
            except Exception as e:
                print(f"[ERROR] Could not delete: {e}")
    else:
        print("[ERROR] Student not found.")

def export_report():
    logs = database.get_logs_by_date(None) # Get all logs
    if not logs:
        print("[ERROR] No logs found in database to export.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_name = f"attendance_report_{timestamp}.csv"
    
    try:
        import csv
        with open(export_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Student Name', 'Date', 'Time', 'Session/Subject'])
            writer.writerows(logs)
        print(f"[SUCCESS] Report exported as: {os.path.abspath(export_name)}")
    except Exception as e:
        print(f"[ERROR] Export failed: {e}")

def search_by_date():
    date_to_find = input("Enter date to search (YYYY-MM-DD): ").strip()
    if not date_to_find:
        print("[ERROR] Date cannot be empty.")
        return
        
    logs = database.get_logs_by_date(date_to_find)
    if not logs:
        print(f"\n[INFO] No records found for {date_to_find}.")
        return

    print("\n" + "="*70)
    print(f"{'Student Name':<20} | {'Date':<12} | {'Time':<10} | {'Subject/Session':<15}")
    print("=" * 70)
    for name, date, time, subject in logs:
        sub = subject if subject else "General/Legacy"
        print(f"{name:<20} | {date:<12} | {time:<10} | {sub:<15}")
    print("=" * 70)

def attendance_summary():
    attendees = database.get_today_summary()
    today = datetime.now().strftime("%Y-%m-%d")
    
    print("\n" + "="*45)
    print(f" ATTENDANCE SUMMARY FOR TODAY ({today}) ")
    print("="*45)
    print(f"Total Students Recognized: {len(attendees)}")
    if attendees:
        print("List: " + ", ".join([a.replace('_', ' ') for a in attendees]))
    print("-" * 45)

def clear_logs():
    confirm = input("Are you sure you want to CLEAR ALL database logs? (y/n): ").lower()
    if confirm == 'y':
        try:
            database.clear_all_logs()
            print("[SUCCESS] All database logs have been cleared.")
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
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        main_menu()
    else:
        print("[INFO] Launching Graphical User Interface...")
        try:
            import gui
            app = gui.App()
            app.mainloop()
        except ImportError as e:
            print(f"[WARNING] GUI launch failed (ImportError): {e}")
            import traceback
            traceback.print_exc()
            print("[INFO] Falling back to terminal menu...")
            main_menu()
        except Exception as e:
            print(f"[ERROR] Could not launch GUI: {e}")
            import traceback
            traceback.print_exc()
            print("[INFO] Falling back to terminal menu...")
            main_menu()
