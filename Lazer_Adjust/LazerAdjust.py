#
#   Author:             Cole Kampa
#   Email:         <kampa041@umn.edu>
#   Institution: University of Minnesota
#   Project:              Mu2e
#   Date:				6/21/17
#
#   Description:
#   A Python 3 script located in Lazer_Adjust folder that edits the .ecp file used for the second half of the straw cutting
#   on the laser. This adjusts the location of each cut in the Y direction to account for length
#   expansion and contraction due to varying temperature and humidity. The temp and humidity are entered
#   in the GLOBAL VARIABLES section (but will eventually be pulled from the website).
#   .csv file to load in with format: Position,   StrawLength(in), Base_x, Base_y, Top_x(pixels),  Top_y(pixels)
#                                     (0,4,2,6,etc)                  (in LaserCut to adjust)  (location on laptop to start click)
#   Pixel locations for .csv file can be determined using mouseLoc.py in MouseLocation
#   NOTE: The straw with the largest y value is the shortest straw
#
#   Modules: pyautogui


import pyautogui
import time
import os
import csv
import sys

#pyautogui.PAUSE = 2 #Might remove after debugging and testing
pyautogui.FAILSAFE = True #Move mouse to top left corner to abort script


##**GLOBAL VARIABLES**##
TEMP = 73.0 #current temp  ##ONLY FOR TESTING
HUMID = 50.0 #current humidity   ##ONLY FOR TESTING

TEMP_INIT = 73.0 #temp for original setting
HUMID_INIT = 27.0 #humidity for original setting

CSV_FILE_04 = 'LaserInfo0,4.csv'
LASERCUT_FILE_04 = 'C2I4.ecp'

CSV_FILE_26 = 'LaserInfo2,6.csv'
LASERCUT_FILE_26 = 'C2I3.ecp'

   
MAIN_DIR = 'C:\\Users\\AP Lazer\\Desktop\\Lazer_Adjust\\' #CSV in CSV_Files, LASERCUT in Original_Lazer_Files
   
X_SIZE = 3 #set pixel amount to adjust to right and down
Y_SIZE = 7
    
C1 = 0.0000094 # Temperature correction
C2 = 0.0000096 # Humidity coefficient

##**FUNCTIONS**##
# Load Data from .csv file into 2d list
def loadData(filename, directory):
    lengths = []
    x_i = []
    y_i = []
    x_start = []
    y_start = []
    with open(directory + filename) as csvf:
        csvReader = csv.reader(csvf)
        firstline = True
        for row in csvReader:
            if firstline:
                firstline = False
                continue
            lengths.append(float(row[1]))
            x_i.append(float(row[2]))
            y_i.append(float(row[3]))
            x_start.append(float(row[4]))
            y_start.append(float(row[5]))
    return lengths, x_i, y_i, x_start, y_start

# pull temp & weather data (TALK TO DAN ON MON ABOUT THIS)
	#look into using urlib to download today file (may need permissions somehow?)
	#read file for last line...then get proper values
	#ambrose0028@gmail.com myacurite.com

# Open LaserCut & .ecp File
def openFile(filename, directory):
    os.system('start C:\\LaserCut53-2816\\LaserCut53.exe')
    time.sleep(4)#wait 4 seconds after opening 
    pyautogui.hotkey('ctrl', 'o')
    time.sleep(1)
    pyautogui.typewrite(MAIN_DIR + directory + filename)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.hotkey('shift', 'f4')   #zoom to table
    
    
def changeLoc (xStartClick, yStartClick, xInit, yInit, stLength):
    #Determining new value of X (will add functionality for changing pallets later)
    #x_new_setting = xInit
    
    #Determining new value of Y
    y_length_init = stLength * (1 + (TEMP_INIT - 68) * C1 + (HUMID_INIT - 0) * C2 )
    y_length_final = stLength * (1 + (TEMP - 68) * C1 + (HUMID - 0) * C2 )
    y_diff = y_length_final - y_length_init
    y_final = yInit - y_diff
    
    # pyautogui.click(###, ###) #click select tool (check location)
    pyautogui.moveTo(xStartClick, yStartClick)
    pyautogui.dragRel(X_SIZE, Y_SIZE)
    pyautogui.press('space')
    #pyautogui.click(619, 416) #click x location
    #pyautogui.typewrite(['backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace'])
    #pyautogui.typewrite(str(x_
    pyautogui.click(686, 416) #click y location
    pyautogui.typewrite(['backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace'])
    pyautogui.typewrite(str(y_final))
    pyautogui.click(641, 460)   # Apply
    pyautogui.click(723, 460)   # Close
    
	
def main():
    cut = input('Cut 0,4 or 2,6? ')
    if cut == '0,4':
        las_file = LASERCUT_FILE_04
        las_dir = 'Cut0,4\\'
        csv_file = CSV_FILE_04
    elif cut == '2,6':
        las_file = LASERCUT_FILE_26
        las_dir = 'Cut2,6\\'
        csv_file = CSV_FILE_26
    else:
        input('Error: not a valid cut type, press enter to exit...')
        sys.exit()
    lengths, x_i, y_i, x_start, y_start = loadData(csv_file, 'CSV_Files\\')
    openFile(las_file, 'Original_Lazer_Files\\' + las_dir)
    # if the y value increases (shorter straw length), start from top, else start from bottom
    # this avoids autogui from accidentally selecting the wrong cut or multiple cuts
    if ((TEMP - TEMP_INIT)*C1 + (HUMID - HUMID_INIT)*C2) > 0:
        for i in range(len(x_i)):
            changeLoc(x_start[i], y_start[i], x_i[i], y_i[i], lengths[i])
    else:
        for i in reversed(range(len(x_i))):
            changeLoc(x_start[i], y_start[i], x_i[i], y_i[i], lengths[i])
    pyautogui.hotkey('ctrl', 'shift', 's')
    time.sleep(0.5)
    pyautogui.typewrite(MAIN_DIR + 'Adjusted_Lazer_Files\\' + las_dir + 'C2_temp' + str(TEMP) + '_humid' + str(HUMID))
    pyautogui.press('enter')


main()
