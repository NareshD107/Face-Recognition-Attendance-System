import cv2
import argparse
import database
import os
import threading
from recognition_engine import RecognitionEngine
import email_utils

def mark_attendance(name, session_id=None):
    """
    Logs the attendance for a recognized face into the SQLite database and sends an email if configured.
    """
    success = database.log_attendance(name, session_id)
    if success:
        print(f"[ATTENDANCE] Logged {name} into database.")
        
        # Trigger email notification
        email = database.get_student_email(name)
        if email:
            print(f"[INFO] Sending email notification to {email}...")
            threading.Thread(target=email_utils.send_attendance_email, args=(email, name)).start()
            
    return success


def run_attendance_system(session_id=None):
    # 1. Initialize recognition engine
    print(f"[INFO] Initializing Recognition Engine (Session ID: {session_id})...")
    engine = RecognitionEngine()
    if not engine.data["encodings"]:
        print(f"[ERROR] No face encodings found. Please run encode_faces.py first.")
        return

    # 2. Initialize video stream
    print("[INFO] Starting video stream...")
    video_capture = cv2.VideoCapture(0)
    
    blink_state = {} 

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("[ERROR] Failed to grab frame")
            break

        # Process frame using the engine
        results, blink_state = engine.process_frame(frame, blink_state)

        for res in results:
            name = res["name"]
            top, right, bottom, left = res["location"]
            confidence = res["confidence"]
            has_blinked = res["has_blinked"]

            # Logic for box color and display name
            if name == "Unknown":
                color = (0, 0, 255) # Red
                display_text = name
            elif not has_blinked:
                color = (0, 255, 255) # Yellow
                display_text = f"{name} ({confidence}%) - Blink!"
            else:
                color = (0, 255, 0) # Green
                display_text = f"{name} ({confidence}%)"
                mark_attendance(name, session_id)

            # Draw UI
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            text_color = (0, 0, 0) if color == (0, 255, 255) else (255, 255, 255)
            cv2.putText(frame, display_text, (left + 6, bottom - 6), font, 0.6, text_color, 1)

        # Display
        cv2.imshow('Face Recognition Attendance', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=int, help="Session ID for SQLite logging")
    args = parser.parse_args()
    
    run_attendance_system(session_id=args.session)
