#!/usr/bin/env python3

import os
import psutil
import wmi
import time
import platform
import threading
from PIL import Image, ImageDraw, ImageFont
import pystray
from windows_toasts import Toast, WindowsToaster

# --- Configuration (Future config file will live here) ---
CHECK_INTERVAL = 3          # seconds between temperature checks
TEMP_CRITICAL  = 85         # °C
TEMP_WARNING   = 75         # °C
TEMP_MILD_WARNING = 60       # °C

# --- Log Setup ---
# Get the folder where the script lives
# __file__ is a Python built-in that means "path to this script"
# os.path.dirname gets the folder containing that file
# os.path.abspath converts it to a full absolute path
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

# Join script folder + logs folder + filename
# os.path.join is the correct way to build paths - works on Windows AND Linux
os.makedirs(os.path.join(SCRIPT_DIR, "logs"), exist_ok=True)
LOG_FILE = os.path.join(SCRIPT_DIR, "logs", "temp_log.txt")

# --- Global (cache heavy objects) ---
FONT_PATH = "C:\\Windows\\Fonts\\arialbd.ttf"
try:
    FONT = ImageFont.truetype(FONT_PATH, 55)
except:
    FONT = ImageFont.load_default()     #fallback if font not found
    
TOASTER = WindowsToaster("CPU Temperature Monitor")



def get_temperature(wmi_conn=None):
    if platform.system() == "Windows":
        temps = wmi_conn.MSAcpi_ThermalZoneTemperature()
        return [(t.CurrentTemperature - 2732) / 10 for t in temps]
    elif platform.system() == "Linux":
        temps = psutil.sensors_temperatures().get("coretemp", [])
        return [t.current for t in temps]
    else:
        return[]


        
def get_status(celsius):
    if celsius > TEMP_CRITICAL:
        return "🔥 CRITICAL!", (255, 60, 60)        # red
    elif celsius > TEMP_WARNING:
        return "🟠 WARNING", (255, 125, 0)           # Orange
    elif celsius > TEMP_MILD_WARNING:
        return "⚠ WARNING Above 60°C", (255, 200, 0)# yellow
    else:
        return "✅ OK", (0, 200, 100)               # green
        
def make_tray_image(celsius, color):
    # creates a 64x64 image with temperature number as the icon
    # PIL = Python Imaging Lirary, lest us draw pixels programmatically
    img = Image.new("RGBA", (64,64), (0,0,0,0))     # Transparent background
    draw = ImageDraw.Draw(img)
    
    # Draw colored circle backgrounddraw
    # draw.ellipse([2,2,63,63], fill=color)
    
    # Draw temperature text centered on circle
    text = str(int(celsius))
    
    # Load windows sytem font at readable size
    
    
    # Default font - we'll upgrade to custom font in future
    draw.text((32, 32), text, fill=color, anchor="mm", font=FONT)
    
    return img
    
def write_log(timestamp, celsius, status_text):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {celsius}°C {status_text}\n")
        
def monitor_loop(icon):
    # This function runs in a seperate threading
   
    if platform.system() == "Windows":
        thread_wmi = wmi.WMI(namespace=r"root\wmi")
    else:
        thread_wmi = None
    
    last_notification = 0       # prevents notification spam
    log_counter = 0
    last_celsius = None
    

    while True:
        readings = get_temperature(thread_wmi)
        timestamp = time.strftime("%H:%M:%S")
        
        if readings:
            celsius = max(readings)
            status_text, color = get_status(celsius)
            
            # Only redraw icon if temperature actually changed
            # Saves CPU cycles when temp is stable
            if celsius != last_celsius:
                icon.icon = make_tray_image(celsius, color)
                icon.title =f"CPU Temp: {celsius}°C {status_text}"
                last_celsius = celsius
            
            print(f"[{timestamp}] Temp: {celsius}°C {status_text}")
            
            # log_counter increases every loop
            # % 5 means only write when counter is divisible by 5
            # So we log every 5th reading instead of every reading
            log_counter += 1 
            if log_counter % 5 == 0:
                write_log(timestamp, celsius, status_text)
            
            # Only notify once per 60 seconds to avoid spam
            current_time = time.time()
            if celsius > TEMP_WARNING and (current_time - last_notification) > 60:
                toast = Toast()
                toast.text_fields = [
                    f"🔥 CPU at {celsius}°C!",
                    "Risk of crash - save your work NOW!"
                ]
                TOASTER.show_toast(toast)
                last_notification = current_time
                
        time.sleep(CHECK_INTERVAL)
        
def open_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("No temperature readings yet.\n")
    # LOG_FILE is now absolute path so startfile always finds it
    os.startfile(LOG_FILE)    # Opens log in default text editor
        
def stop(icon):
    icon.stop()
            
def main():
    # Write session start marker
    session_start = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding ="utf-8") as f:
        f.write(f"\n{'='*40}\n")
        f.write(f"SESSION STARTED: {session_start}\n")
        f.write(f"{'='*40}\n")
        

    print("Temperature Monitor Started...")
    print("Running ins system tray - right click icon to exit")
    print("=" * 40)
    
    # create initial tray icon
    initial_image = make_tray_image(0, (100, 100, 100))
    
    # Tray menue - right clicking icon shows these options
    menu = pystray.Menu(
        pystray.MenuItem("Open Log File", lambda: open_log()),
        pystray.MenuItem("Exit", lambda icon, item: stop(icon))
    )
    
    icon = pystray.Icon(
        "cpu_temp",
        initial_image,
        "CPU Temperature Monitor",
        menu
    )
    
    # Start monitor in background threading
    # daemon=True means thread dies automatically when main program exits
    thread = threading.Thread(target=monitor_loop, args=(icon,), daemon=True)
    thread.start()
    
    # Run tray icon (this locks unitl exist is clicked)
    icon.run()
    
    # Write session end marker when exiting
    session_end = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{'='*40}\n")
        f.write(f"SESSION ENDED: {session_end}\n")
        f.write(f"{'='*40}\n")
    print("\nMonitor Stopped.")
    
        
if __name__ == "__main__":
    main()


