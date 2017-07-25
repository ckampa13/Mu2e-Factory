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
- Script: [StrawResistanceMeasurement.py](Resistance_Measurement/Manual/StrawResistanceMeasurement.py)
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

## glueups:
- Script: [glueups.py](/glueups/glueups.py)
- Language: Python 2.7
- Computer: Epoxying Station
- Description: Program for Mu2e factory workers to enter information about straw gluing.

## make_straw
- Script: [make_straw.py](/make_straw/make_straw.py)
- Language: Python 2.7
- Computer: Tensioning Endpiece Epoxying Station
- Description: Program for workers to initially create straw in database.

## straw_cut_lengths
- Script: [straw_cut_lengths.py](/straw_cut_lengths/straw_cut_lengths.py)
- Language: Python 2.7
- Computer: Straw Length Measuring Station
- Description: Program for Mu2e factory workers to enter length of straws after cutting.

## straw_thicknesses
- Script: [straw_thicknesses.py](straw_thicknesses/straw_thicknesses.py)
- Language: Python 2.7
- Computer: 
- Description: Program for Mu2e factory workers to enter thickness of straws.

## master_upload
- Script: [master_upload.py](/master_upload/master_upload.py)
- Language: Python 2.7
- Computer: Manager's Computer
- Description: Program to find all of the straw data .csv files from the day and upload them to the database.
