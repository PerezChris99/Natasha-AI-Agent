import os
import sys
import subprocess
import platform

def main():
    print("Natasha Assistant Setup")
    print("======================")
    
    # Check Python version
    py_version = sys.version_info
    print(f"Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")
    
    if py_version.major != 3 or py_version.minor < 9:
        print("Warning: This project is recommended to run with Python 3.9+")
        input("Press Enter to continue anyway or Ctrl+C to exit...")

    # Install requirements
    print("\nInstalling base requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Handle PyAudio separately
    if platform.system() == "Windows":
        print("\nFor PyAudio on Windows:")
        print("Please download the appropriate wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
        print(f"For your Python version ({py_version.major}.{py_version.minor}), look for:")
        print(f"PyAudio‑0.2.13‑cp{py_version.major}{py_version.minor}‑cp{py_version.major}{py_version.minor}‑win_amd64.whl")
        
        wheel_path = input("\nEnter the path to the downloaded PyAudio wheel (or press Enter to skip): ")
        if wheel_path and os.path.exists(wheel_path):
            subprocess.run([sys.executable, "-m", "pip", "install", wheel_path])
        else:
            print("Skipping PyAudio installation for now.")
    
    # Try to install other requirements
    print("\nInstalling other requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("\nSetup completed!")
    print("If you encountered any errors, please check the install_instructions.md file.")

if __name__ == "__main__":
    main()
