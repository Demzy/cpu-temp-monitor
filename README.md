# CPU Temperature Monitor

A lightweight Python tool that monitors CPU temperature in real time,
displays live readings in the system tray, logs history to a file,
and sends desktop notifications on high temperatures.

## Part of a Three-Tool Ecosystem
Part 1 of a system health monitoring suite:
- Part 1: temperature_check.py — real-time monitoring (this tool) ✅
- Part 2: log_formatter.py — universal log parser (in development)
- Part 3: crash_analyzer.py — crash diagnosis and fixes (planned)

## Current Features
- Live temperature in system tray icon (colour coded)
- Three threshold levels: Mild Warning / Warning / Critical
- Desktop toast notifications on high temperature
- Session markers for crash forensics
- System snapshot on CRITICAL only (CPU%, RAM%, top 3 processes)

## Dependencies
pip install wmi psutil pystray pillow windows-toasts

## Usage
Run as administrator:
python temperature_check.py

## Thresholds (configurable at top of file)
- Above 60°C: Mild Warning
- Above 75°C: Warning
- Above 85°C: Critical

## Roadmap
- [ ] JSON structured logging
- [ ] System snapshot on CRITICAL only
      (CPU%, RAM%, top 3 processes)
- [ ] Startup task installer
- [ ] LibreHardwareMonitor for accurate temps
- [ ] Config file for thresholds
- [ ] Settings menu in system tray
- [ ] macOS support
- [ ] Adaptive monitoring intervals
