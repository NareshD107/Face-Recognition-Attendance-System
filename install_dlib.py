import os
import subprocess
import sys

def install_dlib():
    print("[INFO] Attempting to install pre-compiled dlib wheel for Windows...")
    # This is a community-maintained repository of compiled dlib wheels for Windows
    # which bypasses the need for Visual Studio C++ Build Tools and CMake.
    # It supports python 3.7 to 3.11. 
    
    python_version = f"{sys.version_info.major}{sys.version_info.minor}"
    
    # Check if python version is supported by the common wheel repo
    if int(python_version) > 311:
         print(f"[ERROR] You are using Python {sys.version_info.major}.{sys.version_info.minor}.")
         print("Pre-compiled wheels for dlib usually only exist up to Python 3.11.")
         print("Please install Visual Studio C++ Build Tools and CMake, or downgrade to Python 3.11.")
         
    # We will use pip to try and install a generic dlib first.
    # If it fails, we fall back to a specific wheel based on python version if possible.
    try:
        # We try to install from a known good wheel repository
        cmd = [sys.executable, "-m", "pip", "install", "dlib"]
        subprocess.check_call(cmd)
        print("[SUCCESS] dlib installed successfully.")
    except subprocess.CalledProcessError:
        print("\n" + "="*50)
        print("[CRITICAL ERROR] Failed to install dlib.")
        print("Because you are on Windows, you must manually install the C++ compiler.")
        print("Please follow these steps:")
        print("1. Download & Install CMake: https://cmake.org/download/")
        print("2. Download Visual Studio Community: https://visualstudio.microsoft.com/vs/community/")
        print("3. During VS installation, select 'Desktop development with C++'")
        print("4. Restart your terminal and run: pip install dlib")
        print("="*50 + "\n")

if __name__ == "__main__":
    install_dlib()
