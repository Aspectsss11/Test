import os
import subprocess

def install(package):
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", package])

def main():
    print("Installing required libraries...")
    libraries = [
        "opencv-python",   # For cv2
        "numpy",           # For array processing
        "pypiwin32",       # For win32api
        "dxcam",           # For screen capture
        "keyboard",        # For hotkey management
        "psutil",          # For process management
        "socket",          # For networking
        "threading",       # For multithreading
        "time",            # For timing functionalities
        "random",          # For random number generation
        "hashlib",         # For generating hashes
        "ctypes",          # For working with Windows libraries
        "json"             # For configuration handling
    ]

    for lib in libraries:
        try:
            install(lib)
            print(f"{lib} installed successfully")
        except Exception as e:
            print(f"Failed to install {lib}: {e}")

    print("All libraries installed")

if __name__ == "__main__":
    main()
