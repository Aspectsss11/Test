import json
import time
import threading
import keyboard
import sys
import win32api
import random
import hashlib
from ctypes import WinDLL
import numpy as np
import socket
import dxcam
import cv2
import psutil
import os

# Set up a socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 65432))

def generate_signature():
    """Generate a unique signature based on time, randomness, and hashing."""
    random_value = random.randint(100000, 999999)
    current_time = time.time()
    data = f"{random_value}-{current_time}".encode()
    return hashlib.sha256(data).hexdigest()

# Store the generated signature
SESSION_SIGNATURE = generate_signature()
print(f"Session Signature: {SESSION_SIGNATURE}")

def safe_exit():
    try:
        exec(type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '', 0, b''))  # Fallback for forced exit
    except:
        try:
            sys.exit()
        except:
            raise SystemExit

# Initialize Windows libraries for DPI awareness and screen size retrieval
user32, kernel32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("kernel32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

shcore.SetProcessDpiAwareness(2)
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Define a screen region to capture for monitoring
OFFSET = 5
GRAB_AREA = (
    int(WIDTH / 2 - OFFSET),
    int(HEIGHT / 2 - OFFSET),
    int(WIDTH / 2 + OFFSET),
    int(HEIGHT / 2 + OFFSET),
)

class EventMonitor:
    def __init__(self):
        self.camera = dxcam.create(output_idx=0)  # Initialize dxcam
        self.monitor_active = False
        self.ready_to_toggle = True
        self.stop_program = False
        self.toggle_lock = threading.Lock()
        self.fake_input = 'k'  # Dummy payload

        # Load configuration
        with open('config.json') as config_file:
            settings = json.load(config_file)

        try:
            self.hotkey = int(settings["trigger_hotkey"], 16)
            self.always_on = settings["always_enabled"]
            self.delay_percent = settings["trigger_delay"]
            self.base_delay = settings["base_delay"]
            self.tolerance = settings["color_tolerance"]
            self.target_color = (250, 100, 250)  # RGB for purple
            self.fps = settings["fps"]  # FPS setting from config
            self.turbo_mode = settings.get("turbo_mode", False)  # Get turbo mode from config
            self.priority = settings.get("priority", "normal")  # Get priority from config
        except:
            safe_exit()

        # Apply priority setting
        self.set_priority()

        # If turbo mode is enabled, reduce delays
        if self.turbo_mode:
            self.base_delay *= 0.5  # 50% faster
            self.delay_percent *= 0.5

        self.frame_duration = 1 / self.fps  # FPS control

    def set_priority(self):
        """Set process priority to high or normal based on config."""
        p = psutil.Process(os.getpid())
        if self.priority == "high":
            p.nice(psutil.HIGH_PRIORITY_CLASS)
            print("Priority set to HIGH")
        elif self.priority == "normal":
            p.nice(psutil.NORMAL_PRIORITY_CLASS)
            print("Priority set to NORMAL")
        else:
            print("Invalid priority setting. Using default.")

    def reset_toggle(self):
        time.sleep(0.1)
        with self.toggle_lock:
            self.ready_to_toggle = True
            kernel32.Beep(440, 75), kernel32.Beep(700, 100) if self.monitor_active else kernel32.Beep(440, 75), kernel32.Beep(200, 100)

    def scan_area(self):
        """Capture the screen and scan for the target color."""
        img = self.camera.grab(region=GRAB_AREA)  # Use dxcam to grab the region
        if img is None:
            return  # Skip if no frame is captured

        pixels = np.array(img).reshape(-1, 3)
        match = (
            (pixels[:, 0] > self.target_color[0] - self.tolerance) & (pixels[:, 0] < self.target_color[0] + self.tolerance) &
            (pixels[:, 1] > self.target_color[1] - self.tolerance) & (pixels[:, 1] < self.target_color[1] + self.tolerance) &
            (pixels[:, 2] > self.target_color[2] - self.tolerance) & (pixels[:, 2] < self.target_color[2] + self.tolerance)
        )
        matching_pixels = pixels[match]

        if self.monitor_active and len(matching_pixels) > 0:
            total_delay = self.base_delay * (1 + self.delay_percent / 100.0)
            time.sleep(total_delay)
            sock.send(self.fake_input.encode())

    def toggle_monitor(self):
        if keyboard.is_pressed("f10"):
            with self.toggle_lock:
                if self.ready_to_toggle:
                    self.monitor_active = not self.monitor_active
                    print(f"Monitor Active: {self.monitor_active}")
                    print(f"Signature: {SESSION_SIGNATURE}")  # Optional logging
                    self.ready_to_toggle = False
                    threading.Thread(target=self.reset_toggle).start()

        if keyboard.is_pressed("ctrl+shift+x"):
            self.stop_program = True
            safe_exit()

    def key_hold_loop(self):
        while True:
            while win32api.GetAsyncKeyState(self.hotkey) < 0:
                self.monitor_active = True
                self.scan_area()
                time.sleep(self.frame_duration)  # Apply FPS control here
            else:
                time.sleep(0.1)

            if keyboard.is_pressed("ctrl+shift+x"):
                self.stop_program = True
                safe_exit()

    def main_loop(self):
        while not self.stop_program:
            if self.always_on:
                self.toggle_monitor()
                self.scan_area() if self.monitor_active else time.sleep(self.frame_duration)  # Apply FPS control here
            else:
                self.key_hold_loop()

# Start the event monitor
EventMonitor().main_loop()
import json
import time
import threading
import keyboard
import sys
import win32api
import random
import hashlib
from ctypes import WinDLL
import numpy as np
import socket
import dxcam
import cv2
import psutil
import os

# Set up a socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 65432))

def generate_signature():
    """Generate a unique signature based on time, randomness, and hashing."""
    random_value = random.randint(100000, 999999)
    current_time = time.time()
    data = f"{random_value}-{current_time}".encode()
    return hashlib.sha256(data).hexdigest()

# Store the generated signature
SESSION_SIGNATURE = generate_signature()
print(f"Session Signature: {SESSION_SIGNATURE}")

def safe_exit():
    try:
        exec(type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '', 0, b''))  # Fallback for forced exit
    except:
        try:
            sys.exit()
        except:
            raise SystemExit

# Initialize Windows libraries for DPI awareness and screen size retrieval
user32, kernel32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("kernel32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

shcore.SetProcessDpiAwareness(2)
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Define a screen region to capture for monitoring
OFFSET = 5
GRAB_AREA = (
    int(WIDTH / 2 - OFFSET),
    int(HEIGHT / 2 - OFFSET),
    int(WIDTH / 2 + OFFSET),
    int(HEIGHT / 2 + OFFSET),
)

class EventMonitor:
    def __init__(self):
        self.camera = dxcam.create(output_idx=0)  # Initialize dxcam
        self.monitor_active = False
        self.ready_to_toggle = True
        self.stop_program = False
        self.toggle_lock = threading.Lock()
        self.fake_input = 'k'  # Dummy payload

        # Load configuration
        with open('config.json') as config_file:
            settings = json.load(config_file)

        try:
            self.hotkey = int(settings["trigger_hotkey"], 16)
            self.always_on = settings["always_enabled"]
            self.delay_percent = settings["trigger_delay"]
            self.base_delay = settings["base_delay"]
            self.tolerance = settings["color_tolerance"]
            self.target_color = (250, 100, 250)  # RGB for purple
            self.fps = settings["fps"]  # FPS setting from config
            self.turbo_mode = settings.get("turbo_mode", False)  # Get turbo mode from config
            self.priority = settings.get("priority", "normal")  # Get priority from config
        except:
            safe_exit()

        # Apply priority setting
        self.set_priority()

        # If turbo mode is enabled, reduce delays
        if self.turbo_mode:
            self.base_delay *= 0.5  # 50% faster
            self.delay_percent *= 0.5

        self.frame_duration = 1 / self.fps  # FPS control

    def set_priority(self):
        """Set process priority to high or normal based on config."""
        p = psutil.Process(os.getpid())
        if self.priority == "high":
            p.nice(psutil.HIGH_PRIORITY_CLASS)
            print("Priority set to HIGH")
        elif self.priority == "normal":
            p.nice(psutil.NORMAL_PRIORITY_CLASS)
            print("Priority set to NORMAL")
        else:
            print("Invalid priority setting. Using default.")

    def reset_toggle(self):
        time.sleep(0.1)
        with self.toggle_lock:
            self.ready_to_toggle = True
            kernel32.Beep(440, 75), kernel32.Beep(700, 100) if self.monitor_active else kernel32.Beep(440, 75), kernel32.Beep(200, 100)

    def scan_area(self):
        """Capture the screen and scan for the target color."""
        img = self.camera.grab(region=GRAB_AREA)  # Use dxcam to grab the region
        if img is None:
            return  # Skip if no frame is captured

        pixels = np.array(img).reshape(-1, 3)
        match = (
            (pixels[:, 0] > self.target_color[0] - self.tolerance) & (pixels[:, 0] < self.target_color[0] + self.tolerance) &
            (pixels[:, 1] > self.target_color[1] - self.tolerance) & (pixels[:, 1] < self.target_color[1] + self.tolerance) &
            (pixels[:, 2] > self.target_color[2] - self.tolerance) & (pixels[:, 2] < self.target_color[2] + self.tolerance)
        )
        matching_pixels = pixels[match]

        if self.monitor_active and len(matching_pixels) > 0:
            total_delay = self.base_delay * (1 + self.delay_percent / 100.0)
            time.sleep(total_delay)
            sock.send(self.fake_input.encode())

    def toggle_monitor(self):
        if keyboard.is_pressed("f10"):
            with self.toggle_lock:
                if self.ready_to_toggle:
                    self.monitor_active = not self.monitor_active
                    print(f"Monitor Active: {self.monitor_active}")
                    print(f"Signature: {SESSION_SIGNATURE}")  # Optional logging
                    self.ready_to_toggle = False
                    threading.Thread(target=self.reset_toggle).start()

        if keyboard.is_pressed("ctrl+shift+x"):
            self.stop_program = True
            safe_exit()

    def key_hold_loop(self):
        while True:
            while win32api.GetAsyncKeyState(self.hotkey) < 0:
                self.monitor_active = True
                self.scan_area()
                time.sleep(self.frame_duration)  # Apply FPS control here
            else:
                time.sleep(0.1)

            if keyboard.is_pressed("ctrl+shift+x"):
                self.stop_program = True
                safe_exit()

    def main_loop(self):
        while not self.stop_program:
            if self.always_on:
                self.toggle_monitor()
                self.scan_area() if self.monitor_active else time.sleep(self.frame_duration)  # Apply FPS control here
            else:
                self.key_hold_loop()

# Start the event monitor
EventMonitor().main_loop()
