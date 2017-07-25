# Mu2e-Factory
A collection of the Python scripts and Arduino sketches used at the various workstations of the Mu2e factory.
To make the script(s) for a given computer easy to access, clone this repository to the Desktop, and create
a shortcut of the .py (.ino, File Directory etc.) file the user should run directly to the Desktop.

## Lazer_Adjust:
- Script: LazerAdjust.py
- Language: Python 3
- Packages: pyautogui, time, os, csv, sys
- Computer: Windows laptop connected to laser cutter
- Description: Adjusts a given LaserCut file to account for the current temperature and humidity.

## Resistance_Measurement:
### Manual:
- Script: StrawResistanceMeasurement.py
- Language: Python 3
- Computer: Windows desktop in back room of 464 with Agilent DMM connected via USB.
- Packages: 
- Description: Measures and records individual straw resistance measurements using Agilent DMM and special probes.	
### Automated:
- Script: StrawResistanceAutomated.ino; StrawResistanceAuto.py
- Language: Arduino; Python 3
- Packages: N/A; pygui (included in folder)
- Computer: Windows desktop in back room of 464 with Arduino connected
- Description: Measures and records straw resistance measurements for an entire pallet automatically. User interface displays straws that pass and fail test.
