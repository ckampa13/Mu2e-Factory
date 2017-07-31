#
#   Author:             Cole Kampa
#   Email:         <kampa041@umn.edu>
#   Institution: University of Minnesota
#   Project:              Mu2e
#   Date:	    	    7/28/17
#
#   Description:
#   A Python 3 script using VISA to control an Arduino Uno and PCB board connected to full pallet of straws. 
#
#   Columns in file (for database): straw_barcode, create_time, worker_barcode, workstation_barcode, resistance, temperature, humidity, test_type
#
#   Packages:
#

import serial
import time

ser = serial.Serial('COM4', 9600)
print (ser.readline())
#print ("\n")

for i in range(0, 16):
    ser.write(bytes(chr(i+97), 'ascii'))
    ser.write(b'r')
    print (ser.readline())



