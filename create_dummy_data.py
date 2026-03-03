import os
import cv2
import numpy as np

# Create dataset subdirectories for two demo users
directories = [
    "dataset/Elon_Musk",
    "dataset/Bill_Gates"
]

for d in directories:
    if not os.path.exists(d):
        os.makedirs(d)

print("[INFO] Creating dummy images (blank colored squares) for testing purposes.")
print("[WARN] Real face recognition requires actual faces. These images will likely fail face_recognition detection, but this script ensures the folder structure is correct.")

# Create some dummy image files to ensure the directory structure is right
# In reality, you'd place real photos here.
# Blue square for Elon
img1 = np.zeros((300, 300, 3), dtype=np.uint8)
img1[:] = (255, 0, 0)
cv2.imwrite("dataset/Elon_Musk/elon_1.jpg", img1)

# Green square for Bill
img2 = np.zeros((300, 300, 3), dtype=np.uint8)
img2[:] = (0, 255, 0)
cv2.imwrite("dataset/Bill_Gates/bill_1.jpg", img2)

print("[SUCCESS] Dummy data directory structure created.")
print("--> Please replace the dummy images in 'dataset/' with real photos of faces before running encode_faces.py")
