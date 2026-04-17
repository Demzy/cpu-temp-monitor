# CPU Temperature Monitor
 
A python tool that monitors CPU temperature in real time, 
logs readings, and warns on high temps are too high

## Requirements
pip install wmi psutil

## Usage
Run as administrator: 
python temperature_check.py

## Output
- Live temperature reading every 10 seconds
- logs daved to temp_log.txt
- status indicators: OK / WARNING / CRITICAL

## platform
Currently supports windows. Linux support via psutil included.
