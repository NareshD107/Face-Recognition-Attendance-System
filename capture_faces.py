import cv2
import os
import time
import database
import argparse

def capture_faces(name=None):
    # 1. Get user name if not provided
    if not name:
        name = input("Enter the name of the person: ").strip().replace(" ", "_")
    
    if not name:
        print("[ERROR] Name cannot be empty.")
        return

    # Add to database
    database.add_student(name)

    # 2. Create directory for the user
    dataset_dir = "dataset"
    user_dir = os.path.join(dataset_dir, name)
    
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
        print(f"[INFO] Created directory: {user_dir}")
    else:
        print(f"[INFO] Directory {user_dir} already exists. Adding images to it.")

    # 3. Initialize webcam
    print("[INFO] Starting video stream. Look at the camera...")
    video_capture = cv2.VideoCapture(0)
    
    # Allow camera to warm up
    time.sleep(2.0)
    
    count = 0
    total_images = 20
    
    print(f"[INFO] Capturing {total_images} images. Please move your head slightly...")

    while count < total_images:
        ret, frame = video_capture.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        # Display the frame
        cv2.putText(frame, f"Captured: {count}/{total_images}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Capturing Faces - Press 'q' to abort", frame)

        # Save the image
        img_name = f"{name}_{count}.jpg"
        img_path = os.path.join(user_dir, img_name)
        cv2.imwrite(img_path, frame)
        print(f"[INFO] Saved {img_path}")
        
        count += 1
        
        # Pause slightly between captures
        time.sleep(0.3)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Capture aborted by user.")
            break

    video_capture.release()
    cv2.destroyAllWindows()
    
    if count == total_images:
        print(f"[SUCCESS] Captured {count} images for {name}.")
        print("[INFO] Next step: Run 'python encode_faces.py' to update the model.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, help="Name of the person to capture")
    args = parser.parse_args()
    
    capture_faces(name=args.name)
