import os
import csv
import shutil
import argparse
import database

def bulk_import(csv_file, images_dir):
    """
    Imports students from a CSV and matches them with images in a directory.
    CSV columns: Name, Roll, Email, Department
    Images should be named after the student or roll number (e.g., "John_Doe.jpg" or "101.jpg")
    """
    print(f"[INFO] Starting bulk import from {csv_file}...")
    
    if not os.path.exists(csv_file):
        print(f"[ERROR] CSV file not found: {csv_file}")
        return

    if not os.path.exists(images_dir):
        print(f"[ERROR] Images directory not found: {images_dir}")
        return

    # Initialize DB
    database.init_db()

    success_count = 0
    fail_count = 0

    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            roll = row.get('Roll', '').strip()
            email = row.get('Email', '').strip()
            dept = row.get('Department', '').strip()

            if not name:
                print("[WARNING] Skipping row with empty name.")
                fail_count += 1
                continue

            name_db = name.replace(" ", "_")
            
            # 1. Register in Database
            database.add_student(name_db, email, roll, dept)
            
            # 2. Match and Copy Images
            # Try matching by name or roll
            found_images = []
            name_clean = name.lower().replace(" ", "_")
            for img_name in os.listdir(images_dir):
                img_name_lower = img_name.lower()
                if name_clean in img_name_lower or (roll and roll in img_name_lower):
                    found_images.append(img_name)
            
            if found_images:
                user_dir = os.path.join("dataset", name_db)
                os.makedirs(user_dir, exist_ok=True)
                for img in found_images:
                    shutil.copy(os.path.join(images_dir, img), os.path.join(user_dir, img))
                print(f"[SUCCESS] Imported {name} with {len(found_images)} images.")
                success_count += 1
            else:
                print(f"[WARNING] No images found for {name} ({roll}) in {images_dir}")
                fail_count += 1

    print("\n" + "="*30)
    print(f"Bulk Import Completed")
    print(f"Successfully Imported: {success_count}")
    print(f"Failed/Skipped: {fail_count}")
    print("="*30)
    print("[INFO] Please run 'Generate Face Encodings' to update the model.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk Import Students from CSV and Images")
    parser.add_argument("--csv", required=True, help="Path to the CSV file")
    parser.add_argument("--images", required=True, help="Path to the images directory")
    args = parser.parse_args()
    
    bulk_import(args.csv, args.images)
