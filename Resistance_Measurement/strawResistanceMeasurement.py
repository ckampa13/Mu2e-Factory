#
#   Author:             Cole Kampa
#   Email:         <kampa041@umn.edu>
#   Institution: University of Minnesota
#   Project:              Mu2e
#   Date:				6/19/17
#
#   Description:
#   A Python 3 script using VISA to control an Agilent 34410A Digital MultiMeter (DMM). After scanning in the 
#   worker code & workstation code, the user scans the straw number (st#####), then is prompted for each
#   measurement: inside to inside (I-I), outside to outside (O-O), inside to outside (I-O), and outside to inside (O-I). 
#   To take a given measurement (the minimum of 30 data points), press enter. To stop measurements, enter 'q' in straw prompt.
#   Data is saved in comma-delimited format to file: Desktop\\strawResistanceMeasurements\\strawResistance_MM-DD-YY.csv
#   Columns in file (for database): straw_barcode, create_time, worker_barcode, workstation_barcode, resistance, temperature, humidity, test_type
#
#   Libraries: pyvisa (with NI-VISA backend) 
#

import visa
import time
from datetime import datetime

##**Functions**##
def res_meas():
    num = 0
    overload = 0
    res = []
    while (num < 30 and overload < 3):
        val = dmm.query_ascii_values('MEAS:RES?')
        res.extend(val)
        time.sleep(0.1)
        num += 1 
        if (val[0] >= 9e37):
            overload += 1
    if (overload == 3):
        return 'inf'
    else:
        return min(res)
		

##**Global Variables**##
dataDirectory = 'C:\\Users\\LArTPC\\Desktop\\strawResistanceMeasurements\\'
dataFile = 'strawResistance_' + datetime.now().strftime('%m-%d-%Y') + '.csv'
# Test Types (may need to change for database)
ii_type = 'inside-inside'
oo_type = 'outside-outside'
io_type = 'inside-outside'
oi_type = 'outside-inside'


##**Initializing VISA & DMM**##
rm = visa.ResourceManager()
dmm = rm.open_resource('USB0::0x0957::0x0607::MY47003138::INSTR')
dmm.write("*rst; status:preset; *cls")


##**User Interface**##
print('Straw Resistance Measurements:\n')
# Barcode scanning functionality to be added
worker = input ('Scan worker ID: ')
workstation = input ('Scan workstation ID: ')
# temp and humidity auto-load functionality to be added
temp = input('Enter the temperature: ')
humid = input('Enter the humidity: ')

straw = input('Scan straw ID (or \'q\' to quit): ')

with open(dataDirectory + dataFile, 'a') as f:
    #f.write('straw_barcode, create_time,         worker_barcode, workstation_barcode, resistance, temperature, humidity, test_type\n')
    while (straw != 'q'):
        # ii measurement
        input('Press ENTER to collect Inside-Inside (I-I) measurement... ')
        ii = res_meas()
        ii = str(ii)
        print('I-I (Ohms) = ' + ii + '\n')
        # oo measurement
        input('Press ENTER to collect Outside-Outside (O-O) measurement... ')
        oo = res_meas()
        oo = str(oo)
        oo = oo.lstrip('[')
        oo = oo.rstrip(']')
        print('O-O (Ohms) = ' + oo + '\n')
        # io measurement
        input('Press ENTER to collect Inside-Outside (I-O) measurement... ')
        io = res_meas()
        io = str(io)
        print('I-O (Ohms) = ' + io + '\n')
		# oi measurement
        input('Press ENTER to collect Outside-Inside (O-I) measurement... ')
        oi = res_meas()
        oi = str(oi)
        oi = oi.lstrip('[')
        oi = oi.rstrip(']')
        print('O-I (Ohms) = ' + oi + '\n')
        
        # Write to file!
        f.write(straw + ',       ' + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ',   ' + worker + ',         ' + workstation + ',   ' + ii + ',   ' + temp + ',   ' + humid + ',   ' + ii_type + '\n')
        f.write(straw + ',       ' + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ',   ' + worker + ',         ' + workstation + ',   ' + io + ',   ' + temp + ',   ' + humid + ',   ' + io_type + '\n')
        f.write(straw + ',       ' + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ',   ' + worker + ',         ' + workstation + ',   ' + oo + ',   ' + temp + ',   ' + humid + ',   ' + oo_type + '\n')
        f.write(straw + ',       ' + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ',   ' + worker + ',         ' + workstation + ',   ' + oi + ',   ' + temp + ',   ' + humid + ',   ' + oi_type + '\n\n')		
        
		# Start new straw or quit
        straw = input('Enter Straw Number (or \'q\' to quit): ')

input('Quitting program, press ENTER...')



