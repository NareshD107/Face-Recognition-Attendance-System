# 🤖 Face Recognition Attendance System (v4.0)

This project is a high-performance Deep Learning pipeline for real-time face recognition, featuring liveness detection, professional student management, and department-level analytics.

## ✨ Key Features
- **📸 Smart Recognition**: Real-time detection with **Confidence Score (%)** display.
- **👁️ Liveness Detection**: Advanced blink detection to prevent photo-spoofing.
- **� Bulk Student Import**: Register hundreds of students instantly via CSV and image folders.
- **📊 Interactive Analytics**: Professional dashboard with attendance trends and **Department Distribution** charts.
- **� Email Notifications**: Automated attendance confirmation emails to students.
- **📄 Export Options**: Generate reports in both **CSV** and **PDF** formats.

## � Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Automatic Launcher**:
   The easiest way to run the app in your local environment:
   ```bash
   python run_app.py
   ```

## 📋 System Options
The system features a 14-point professional menu:
1. **🖼️ Capture Faces**: Quick registration via camera.
2. **🧬 Generate Encodings**: Update the AI model with new faces.
3. **🚀 Start Attendance**: Launch the live tracking system.
4. **📖 View Logs**: Check recorded attendance.
5. **📝 Register Student**: Full profile registration (Name, Roll, Dept, Email).
6. **🔍 View Students**: List all registered individuals.
7. **🔄 Update Details**: Modify student profiles.
8. **🗑️ Delete Data**: Securely remove records.
9. **📥 Export Report**: Save to CSV/PDF.
10. **📅 Search by Date**: Filter historical data.
11. **📈 Live Summary**: Quick daily attendance count.
12. **🧹 Clear Logs**: Reset database logs.
13. **📷 Camera Check**: Hardware diagnostic tool.
14. **❌ Exit**: Securely close the application.

## ⚙️ Advanced Setup

### 🧠 Generating Encodings
Before running the tracker, the system must process your `dataset` folder:
```bash
python encode_faces.py
```

### � Bulk Importing
To import a large batch of students:
```bash
python bulk_import.py --csv students.csv --images images_folder/
```

## 🏗️ Technical Architecture
- **Core Engine**: Centralized class in `recognition_engine.py` for detection and matching.
- **Frontend**: Modern GUI built with `CustomTkinter`.
- **Backend**: `SQLite3` database for persistence.
- **Computer Vision**: Powered by `OpenCV`, `dlib`, and `face_recognition`.

## 🛠️ Troubleshooting
- **❌ ModuleNotFoundError**: Always use `python run_app.py` to ensure the virtual environment is used.
- **⚠️ Lighting**: Face recognition performance depends heavily on clear lighting.
- **🐢 Performance**: Frames are resized to 1/4 size automatically for high FPS tracking.
