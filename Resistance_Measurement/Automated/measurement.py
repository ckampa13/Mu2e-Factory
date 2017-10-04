#                                                                             *
#   Author:             Cole Kampa
#   Email:         <kampa041@umn.edu>
#   Institution: University of Minnesota
#   Project:              Mu2e
#   Date:	        8/25/17
#   Most Recent Update: 10/2/17 -CK
#
#   Description:
#   A Python 3 script using PySerial to control and read from an Arduino
#   Uno and PCB connected to full pallet of straws. 
#
#   Columns in file (for database): straw_barcode, create_time, 
#   worker_barcode, workstation_barcode, resistance, temperature,
#   humidity, test_type, pass/fail
#
#   Packages: PySerial, colorama
#
#   general order: arbrcrdrerfrgrhrirjrkrlrmrnrorpr
#
#   adjusted order: 1)erfrgrhr 2)arbrcrdr 3)mrnrorpr 4)irjrkrlr

import serial
from datetime import datetime
import time
import csv
import sys
import os
# pip install colorama should work fine
import colorama
from colorama import Back#, Fore, Style

#set a larger window size
os.system('mode con: cols=115 lines=50')


##-Global Variables-##
inf_low_limit = 1000.0 #determining if io and oi measurements are open circuits
ii_pass_range = [150.0,250.0]
oo_pass_range = [50.0,150.0]

com_port = 'COM3'
#com_port = 'COM11'

#calib_file = 'calib_testing.csv'
calib_file = 'Calibration\\calib.csv'
#calib_file_adjusted = 'Calibration\\calib_adjusted.csv'
dataFile = 'Resistance_Data\\StrawResistance_' + datetime.now().strftime('%Y-%m-%d_%H%M%S') + '.csv'
dataFile_adjusted = 'Resistance_Data\\StrawResistance_' + datetime.now().strftime('%Y-%m-%d_%H%M%S') + '_ADJUSTED_CALIB.csv'

meas_cycles = 'abcdefghijklmnop'


#avg_method = 'minimum'
avg_method = 'average'
#   'average' for a strict averaging of resistance values, 'minimum'
#   for minimum measured resistance (max measured voltage)

straw_nums = ['01','02','03','04','05','06','07','08','09','10','11','12',
              '13','14','15','16','17','18','19','20','21','22','23','24']


##STARTING ARDUINO CONNECTION##
ser = serial.Serial(com_port, 9600)
print(ser.readline().decode('utf-8').rstrip())

def gather_info():
    worker = input("Scan worker ID: ")
    workstation = input ("Scan workstation ID: ")
    temp = input ("Enter current temperature (F): ")
    humid = input ("Enter current percent humidity (###.##): ")
    str_start = input ("Scan straw ID for straw 1 (bottom of pallet): ")
    str_end = input ("Scan straw ID for straw 24 (top of pallet): ")
    return worker, workstation, temp, humid, str_start, str_end

#meas_cycles is a string containing characters a-p in desired order
def measure_resistance(avg_type, meas_cycles, straw_start, straw_end, c_file):
    ###--TESTING--###
    first_straw = {'a':'01ii','b':'01io','c':'01oi','d':'01oo', 'e':'02ii','f':'02io','g':'02oi','h':'02oo',
                   'i':'03ii','j':'03io','k':'03oi','l':'03oo', 'm':'04ii','n':'04io','o':'04oi','p':'04oo'}
    ##------------###
    
    #first_straw = {'a':'02ii','b':'02io','c':'02oi','d':'02oo', 'e':'01ii','f':'01io','g':'01oi','h':'01oo',
    #               'i':'04ii','j':'04io','k':'04oi','l':'04oo', 'm':'03ii','n':'03io','o':'03oi','p':'03oo'}

    #creating iterable dictionary of key: straw # (1-24) and value: [strawID, measuredBits]
    straw_ids = {}
    i = 1
    if int(straw_start[2:]) <= int(straw_end[2:]):
        s1 = int(straw_start[2:])
        s24 = int(straw_end[2:])
    else:
        s1 = int(straw_end[2:])
        s24 = int(straw_start[2:])
        
    for x in range(s1,s24+1):
        straw_ids[i] = 'st' + str('%05d'%(x))
        i += 1
    
    #setting averaging method 
    if avg_type == 'average':
        ser.write(b'y')
    elif avg_type == 'minimum':
        ser.write(b'z')
    #getting calibration info
    Vin, V5, r2_list, meas_dict = calibration_store(c_file)

    '''
    ###TESTING###
    i = 1
    for key, value in sorted(meas_dict.items()):
        print('[' + key + ': ' + str(value[0]) + ', ' + str(value[1]) + ']', end='')
        if i % 4 == 0:
            print()
        else:
            print(', ', end='')
        i += 1
    input("Check calibration vals (hit enter)...")
    ################
    '''
    
    #Storing straw ID in meas_dict value index 2
    for key, value in meas_dict.items():
        value[2] = straw_ids[int(key[:2])]
    
    #Measure!
    for char in meas_cycles:
        straw1 = int(first_straw[char][:2])
        measuring = first_straw[char][2:]
        straws = {str('%02d'%(straw1))+measuring:0, str('%02d'%(straw1+4))+measuring:0,
                  str('%02d'%(straw1+8))+measuring:0, str('%02d'%(straw1+12))+measuring:0,
                  str('%02d'%(straw1+16))+measuring:0, str('%02d'%(straw1+20))+measuring:0}
        ser.write(bytes(char+'r', 'ascii')) #send signal to switch to new cycle, then read
        bits_list = ser.readline().decode('utf-8').rstrip().split(',')
        if bits_list[0] != char:
            print('Error! The wrong measurement was collected from the arduino!')
            input('Enter to exit...')
            sys.exit(0)
        del bits_list[0]
        i = 0
        #we must sort straws dict otherwise python iterates over it randomly :( Fixed 9/28/17
        for key, v_out in sorted(straws.items()):
            v_out = float(bits_list[i])*V5/1023.0

            '''
            ##TESTING##
            print(key + ', ' + str(bits_list[i]) + ', ' + str(v_out))
            if (i+1) % 6 == 0:
                input()
            ###########
            '''

            
            i += 1
            #straws dictionary now contains key: straw#+measurement type and value: measured voltage
            if v_out != 0:
                meas_dict[key][3] = float(r2_list[(int(key[:2])-1)//4]) * (V5 - v_out) / v_out
            else:
                meas_dict[key][3] = 1000000
            ############
            #TESTING with partially good calib file
            if float(meas_dict[key][0]) != 1:
                meas_dict[key][4] = meas_dict[key][3] / (1 - float(meas_dict[key][0])) - float(meas_dict[key][1])
            else:
                meas_dict[key][4] = meas_dict[key][3]
            ############
            #meas_dict[key][4] = meas_dict[key][3] / (1 - float(meas_dict[key][0])) - float(meas_dict[key][1])
            
            #check if measurement meets 'inf' requirements
            if (float(meas_dict[key][4]) >= inf_low_limit or float(meas_dict[key][4]) <= 1):
                meas_dict[key][4] = 'inf'
            meas_dict[key][5] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            #determines and stores pass/fail
            meas_dict[key][6] = check_measurement(key, float(meas_dict[key][4]))
        for key, value in sorted(meas_dict.items()):
            value[6] = check_measurement(key,value[4])
    return meas_dict
        
    

def calibration_store(calib_f):
    r2_list = []
    calib_dict = {}
    with open(calib_f) as csvf:
        csvReader = csv.reader(csvf)
        header = True
        calib = ('volt','res','err')
        index = 0
        firstline = True
        for row in csvReader:
            if firstline:
                firstline = False
                continue
            if str(row[0])[0] == '*':
                index += 1
                continue
            if calib[index] == 'volt':
                Vin,V5 = row[0], row[1]
            elif calib[index] == 'res':
                r2_list = (row[0], row[1], row[2], row[3], row[4], row[5])
            elif calib[index] == 'err':
                #IMPORTANT FORMATTING
                calib_dict[row[0]] = [row[1],row[2],'',0,0,'',''] #0perc err, 1device resistance, 2strawID 3measured resistance, 4adjusted resistance, 5time stamp, 6pass/fail
    return float(Vin), float(V5), r2_list, calib_dict
    
def check_measurement(key, value):
    if key[2:4] == 'ii':
        if str(value) == 'inf':
            return 'fail'
        if ii_pass_range[0] <= value <= ii_pass_range[1]:
            return 'pass'
        else:
            return 'fail'
    elif key[2:4] == 'io':
        if str(value) == 'inf':
            return 'pass'
        else:
            return 'fail'
    elif key[2:4] == 'oi':
        if str(value) == 'inf':
            return 'pass'
        else:
            return 'fail'
    elif key[2:4] == 'oo':
        if str(value) == 'inf':
            return 'fail'
        if oo_pass_range[0] <= value <= oo_pass_range[1]:
            return 'pass'
        else:
            return 'fail'
    
def display_resistance(straw_dictionary):
    #TESTING#
    print()
    print('#/Type   Ohms    p/f ')
    print('---------------------')
    i = 1
    for key, value in sorted(straw_dictionary.items()):
        print('(' + str(key) + ': ' , end='')
        #print('(' + str(key) + ', ' + str(value[2]) + ': [' , end='')
        #this if statement just formats the printing to look pretty
        if str(value[4]) == 'inf':
            print('%7s' % str(value[4]), end='')
        else:
            print('%7.2f' % float(value[4]), end='')
        print(', ', end='')
        #this prints pass/fail with corresponding colors
        if value[6] == 'pass':
            print(Back.GREEN, end='')
        else:
            print(Back.RED, end='')
        print(value[6] + Back.RESET + ')', end='')
        #every four measurements, print a new line
        if i%4 == 0:
            print()
        else:
            print(', ', end='')
        
        i += 1
        #print(str(key) + ': ' + str(value))
        #print(value[2] + ', ' + str(value[3]) + 'Ohms, ' + str(value[4]) + 'Ohms, ' + value[0][2:3] + '\n')
    
def check_repeat():
    check = input("\n" + "Do these measurements pass (y/n)? ")
    if check == 'y':
        return False
    else:
        print("Repeating measurements...\n")
        return True

def save_resistance(worker, workstation, temp, humid, straw_dictionary,save_file):
    print("Saving file...\n")
    data_file = 'straw_resistance_' + datetime.now().strftime("%Y-%m-%d_%H%M%S_") + workstation + '.csv' 
    with open(save_file, 'a') as f:
        f.write('Straw Id,   Timestamp,    Worker ID,     Workstation Id,  Resistance(Ohms),  Temp(F),  Humidity(%), Measurement Type, Pass/Fail \n')  
        for key, value in sorted(straw_dictionary.items()):
            if key[2:4] == 'ii':
                meas_type = 'inside-inside'
            elif key[2:4] == 'io':
                meas_type = 'inside-outside'
            elif key[2:4] == 'oi':
                meas_type = 'outside-inside'
            elif key[2:4] == 'oo':
                meas_type = 'outside-outside'
            f.write(value[2] + ', ' + value[5] + ', ' + worker + ', ' 
                   + workstation + ', ' + str(value[4]) + ', ' + str(temp) 
                   + ', ' + str(humid) + ', ' + meas_type + ', ' + str(value[6]) + '\n')

def main():
    colorama.init() #turn colorama ANSII conversion on
    wrkr, wrkst, temp, humid, str_start, str_end = gather_info()

    straw_dict = {}
    save_dict = {}
    for value in straw_nums:
        save_dict[value+'ii'] = [0,0,'',0,0,0,'fail']  #[% error, device resistance, pass/fail]
        save_dict[value+'io'] = [0,0,'',0,0,0,'fail']  #[% error, device resistance, pass/fail]
        save_dict[value+'oi'] = [0,0,'',0,0,0,'fail']  #[% error, device resistance, pass/fail]
        save_dict[value+'oo'] = [0,0,'',0,0,0,'fail']  #[% error, device resistance, pass/fail]

    #print('Using first calibration file...\n')
    repeat = True
    while(repeat == True):
        input("Press enter to measure resistance...")
        straw_dict = measure_resistance(avg_method, meas_cycles,
                                        str_start, str_end,calib_file)
        i = 0
        for key, value in sorted(save_dict.items()):
            #if value[6] != 'pass': #and straw_dict[key][6] == 'pass':
            if straw_dict[key][6] == 'pass':
                if key[2:4] == 'ii':
                    better_meas_check = abs(straw_dict[key][4]-200) - abs(value[4]-200)
                elif key[2:4] == 'oo':
                    better_meas_check = abs(straw_dict[key][4]-100) - abs(value[4]-100)
                elif key[2:4] == 'io' or key[2:4] == 'oi':
                    better_meas_check = 1
                if value[6] != 'pass' or better_meas_check < 0:
                    value[0] = straw_dict[key][0]
                    value[1] = straw_dict[key][1]
                    value[2] = straw_dict[key][2]
                    value[3] = straw_dict[key][3]
                    value[4] = straw_dict[key][4]
                    value[5] = straw_dict[key][5]
                    value[6] = straw_dict[key][6]
                    i += 1
        if i == 0:
            repeat = False
        display_resistance(save_dict)
        repeat = check_repeat()
    save_resistance(wrkr, wrkst, temp, humid, save_dict,dataFile)
    input('Press enter to exit...')

    ''' This section was used in testing different calibration methods
    print('Now using adjusted calibration file...\n')
    straw_dict = {}
    save_dict = {}
    for value in straw_nums:
        save_dict[value+'ii'] = [0,0,'',0,0,0,'fail']  #[% error, device resistance, pass/fail]
        save_dict[value+'io'] = [0,0,'',0,0,0,'fail']  #[% error, device resistance, pass/fail]
        save_dict[value+'oi'] = [0,0,'',0,0,0,'fail']  #[% error, device resistance, pass/fail]
        save_dict[value+'oo'] = [0,0,'',0,0,0,'fail']  #[% error, device resistance, pass/fail]

    repeat = True
    while(repeat == True):
        input("Press enter to measure resistance...")
        straw_dict = measure_resistance(avg_method, meas_cycles,
                                        str_start, str_end,calib_file_adjusted)
        i = 0
        for key, value in sorted(save_dict.items()):
            if value[6] != 'pass': #and straw_dict[key][6] == 'pass':
                value[0] = straw_dict[key][0]
                value[1] = straw_dict[key][1]
                value[2] = straw_dict[key][2]
                value[3] = straw_dict[key][3]
                value[4] = straw_dict[key][4]
                value[5] = straw_dict[key][5]
                value[6] = straw_dict[key][6]
                i += 1
        if i == 0:
            repeat = False
        display_resistance(save_dict)
        repeat = check_repeat()
    save_resistance(wrkr, wrkst, temp, humid, save_dict,dataFile_adjusted)
    '''
    
    colorama.deinit()  #turn colorama ANSII conversion off

main()
