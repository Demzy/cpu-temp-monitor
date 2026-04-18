# CPU Temperature Monitor

A lightweight Python tool that monitors CPU temperature in real time,
displays live readings in the system tray, logs history to a file,
and sends desktop notifications on high temperatures.

## Features
- Live temperature in system tray icon (colour coded)
- Three threshold levels: Mild Warning / Warning / Critical
- Desktop toast notifications (Windows)
- Session logging with crash forensics markers
- Cross-platform: Windows (WMI) and Linux (psutil)

## Dependencies
pip install wmi psutil pystray pillow windows-toasts

## Usage
Run as administrator:
python temperature_check.py

## Thresholds (configurable at top of file)
- Above 60°C: Mild Warning
- Above 75°C: Warning  
- Above 85°C: Critical

## Planned Features
- Config file for threshold settings
- LibreHardwareMonitor integration for accuracy
- macOS support
- Settings menu in system tray
