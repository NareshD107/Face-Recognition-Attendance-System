import face_recognition
import os
import cv2
import pickle

KNOWN_FACES_DIR = "dataset"
ENCODINGS_FILE = "encodings.pickle"

def encode_known_faces():
    print("[INFO] Starting face quantification...")
    known_encodings = []
    known_names = []

    # Check if the dataset directory exists
    if not os.path.exists(KNOWN_FACES_DIR):
        print(f"[ERROR] Directory '{KNOWN_FACES_DIR}' not found. Please create it and add face images.")
        return

    # Get list of all images to process first for accurate progress reporting
    image_paths = []
    for name in os.listdir(KNOWN_FACES_DIR):
        dir_path = os.path.join(KNOWN_FACES_DIR, name)
        if not os.path.isdir(dir_path):
            continue
        for filename in os.listdir(dir_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append((name, os.path.join(dir_path, filename)))

    total_images = len(image_paths)
    if total_images == 0:
        print("[WARNING] No images found in dataset. Check your 'dataset/' folder.")
        return

    print(f"[INFO] Found {total_images} images. Processing with optimizations...")

    success_count = 0
    fail_count = 0

    # Loop over the image paths
    for i, (name, image_path) in enumerate(image_paths, 1):
        # Progress update
        print(f"[{i}/{total_images}] Processing {name}/{os.path.basename(image_path)}...", end="\r")
        
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"\n[WARNING] Could not read {image_path}. Skipping.")
                fail_count += 1
                continue
            
            # Performance optimization: Resize large images
            (h, w) = image.shape[:2]
            if w > 1000:
                r = 1000.0 / w
                dim = (1000, int(h * r))
                image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
                
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Detect face locations
            boxes = face_recognition.face_locations(rgb, model="hog")
            
            if not boxes:
                print(f"\n[WARNING] No face found in {image_path}. Ensure face is clear.")
                fail_count += 1
                continue

            # Compute facial embeddings
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(name)
                success_count += 1
        
        except Exception as e:
            print(f"\n[ERROR] processing {image_path}: {e}")
            fail_count += 1

    print(f"\n[INFO] Quantification complete.")
    print(f"[SUMMARY] Successfully encoded: {success_count} faces")
    print(f"[SUMMARY] Failed/Skipped: {fail_count} images")

    # Serialize to disk
    if known_encodings:
        print("[INFO] Serializing encodings to disk...")
        data = {"encodings": known_encodings, "names": known_names}
        with open(ENCODINGS_FILE, "wb") as f:
            pickle.dump(data, f)
        print(f"[SUCCESS] Face database updated: {ENCODINGS_FILE}")
    else:
        print("[ERROR] High-level error: No faces were successfully encoded. Please check your dataset.")

if __name__ == "__main__":
    encode_known_faces()
