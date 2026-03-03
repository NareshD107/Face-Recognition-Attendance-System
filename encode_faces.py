import face_recognition
import os
import cv2
import pickle

KNOWN_FACES_DIR = "dataset"
ENCODINGS_FILE = "encodings.pickle"

def encode_known_faces():
    print("[INFO] Quantifying faces...")
    known_encodings = []
    known_names = []

    # Check if the dataset directory exists
    if not os.path.exists(KNOWN_FACES_DIR):
        print(f"[ERROR] Directory '{KNOWN_FACES_DIR}' not found. Please create it and add face images.")
        return

    # Loop over the image paths
    for name in os.listdir(KNOWN_FACES_DIR):
        dir_path = os.path.join(KNOWN_FACES_DIR, name)
        
        if not os.path.isdir(dir_path):
            continue

        for filename in os.listdir(dir_path):
            image_path = os.path.join(dir_path, filename)
            
            # Load the image and convert it from BGR (OpenCV ordering) to dlib ordering (RGB)
            try:
                image = cv2.imread(image_path)
                if image is None:
                    print(f"[WARNING] Could not read {image_path}. Skipping.")
                    continue
                    
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Detect the (x, y)-coordinates of the bounding boxes corresponding to each face in the input image
                boxes = face_recognition.face_locations(rgb, model="hog") # use "cnn" for more accuracy but slower

                # Compute the facial embedding for the face
                encodings = face_recognition.face_encodings(rgb, boxes)

                # Loop over the encodings (in case there are multiple faces in an image, though usually there should be one)
                for encoding in encodings:
                    known_encodings.append(encoding)
                    known_names.append(name)
            
            except Exception as e:
                print(f"[ERROR] processing {image_path}: {e}")

    # Dump the facial encodings + names to disk
    print("[INFO] Serializing encodings...")
    data = {"encodings": known_encodings, "names": known_names}
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)
    print(f"[SUCCESS] Saved encodings to {ENCODINGS_FILE}")

if __name__ == "__main__":
    encode_known_faces()
