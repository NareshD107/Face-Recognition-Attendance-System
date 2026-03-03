# 🤖 Face Recognition Attendance System

This project is a complete Deep Learning pipeline for recognizing faces in real-time and logging their attendance into a CSV file. 

## ✨ Features
- **📸 Face Recognition**: Real-time detection and recognition using dlib & face_recognition.
- **👥 Student Management**: Register, View, Update, and Delete student records/data.
- **📊 Advanced Reporting**: Export to CSV, Search by Date, and Real-time Summaries.
- **🛠️ System Utilities**: Check camera connection and clear attendance logs.
- **👁️ Blink Detection**: Prevents photo-spoofing during attendance logging.

## 📋 System Options (14-Point Menu)
1. **🖼️ Capture New Faces**: Quick face capture loop.
2. **🧬 Generate Face Encodings**: Update model with new student data.
3. **🚀 Start Attendance System**: Launch live tracking window.
4. **📖 View Attendance Logs**: Terminal-based log viewer.
5. **📝 Register New Student**: Full registration workflow.
6. **🔍 View Registered Students**: List all current students.
7. **🔄 Update Student Details**: Rename existing student records.
8. **🗑️ Delete Student Data**: Clean up old or incorrect student data.
9. **📥 Export Attendance Report**: Save logs to a timestamped file.
10. **📅 Search Attendance by Date**: Filter logs by specific YYYY-MM-DD.
11. **📈 Real-time Attendance Summary**: Quick count of today's attendees.
12. **🧹 Clear Attendance Logs**: Reset log file.
13. **📷 Check Camera Connection**: Verify hardware status.
14. **❌ Exit**: Securely close the application.

## ⚙️ Setup Instructions

### 1. 📦 Install Dependencies
Make sure you have Python 3.7+ installed. 
Depending on your OS (especially Windows), installing `dlib` can be challenging because it requires CMake and a C++ compiler (like Visual Studio Build Tools). 

Run the following command to install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. 📂 Prepare the Dataset
1. Create a folder named `dataset` in the root directory.
2. Inside `dataset`, create a sub-folder for every person you want the system to recognize (e.g., `dataset/John_Doe/`).
3. Place clear, front-facing images of that person inside their respective folder. 
*(You can run `python create_dummy_data.py` to see the expected folder structure).*

### 3. 🧠 Generate Encodings
Before running the live attendance system, the script needs to "learn" the faces. 
Run the following script to process the images in the `dataset` folder and generate the embeddings:
```bash
python encode_faces.py
```
This will create an `encodings.pickle` file containing the recognized facial features.

### 4. 🏃 Run the Attendance System
Once the encodings are generated, you can start the live webcam feed:
```bash
.\venv\Scripts\python.exe main.py
```
- A window will pop up showing the camera feed.
- Recognized faces will have a green box and their name.
- Unknown faces will have a red box labeled "Unknown".
- Press `q` to quit the application.

### 5. 📑 Check Attendance
Open `attendance/attendance.csv` to view the logged attendance records.

## 🛠️ Troubleshooting
- **❌ `dlib` fails to install**: Ensure you have [CMake](https://cmake.org/download/) installed and added to your system PATH. On Windows, install "Desktop development with C++" via the Visual Studio Installer.
- **⚠️ IndexError in `encode_faces.py`**: This means `face_recognition` couldn't find a face in one of the images. Ensure all images clearly show a face.
- **🐢 System is slow/laggy**: Face recognition is computationally heavy. Ensure your lighting is good. By default, `attendance.py` resizes frames to 1/4 size to improve FPS.
