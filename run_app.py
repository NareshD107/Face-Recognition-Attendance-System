import subprocess
import sys
import os

def run_app():
    # Detect the correct python path inside the venv
    if os.name == 'nt': # Windows
        python_path = os.path.join("venv", "Scripts", "python.exe")
    else: # Linux/Mac
        python_path = os.path.join("venv", "bin", "python")

    if not os.path.exists(python_path):
        print(f"[ERROR] Virtual environment (venv) not found at {python_path}")
        print("Please ensure your venv is set up correctly.")
        return

    print(f"[INFO] Using virtual environment: {python_path}")
    print("[INFO] Launching the Attendance System...")
    
    try:
        # Run main.py using the venv's python
        subprocess.run([python_path, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Application exited with error: {e}")
    except KeyboardInterrupt:
        print("\n[INFO] Application closed by user.")

if __name__ == "__main__":
    run_app()
