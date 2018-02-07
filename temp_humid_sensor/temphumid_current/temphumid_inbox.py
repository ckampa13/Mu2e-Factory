
import serial
import time
from time import gmtime
import calendar
from datetime import datetime
import csv
import os

ser = serial.Serial('COM8',9600) #port on computer

#filename ='C:\\Users\\kahn\\Desktop\\temp_humid\\data' + datetime.now().strftime("%Y-%m-%d_%H%M%S")+ '.csv'
filename = 'in_box.csv'

f = open(filename,"w")
print( 'Hit ctrl+c to quit running arduino and save data')

time.sleep(3)

#send character '5' to arduino
#when arduino gets it, it takes data and sends
f.write('date, temp (C), RH (%), epoch time (s)\n') 
try:
	while True:
		ser.write(b'5') # send arduino the number '5' in ascii
		time.sleep(2)	# wait 2 seconds
		data = str(ser.readline() ) # get data from arduino serial
		x = data.split(',')
		temp = x[0]
		humid = x[1]
		humid = humid[:5]
		
		print( "Temp = " + temp + " C  Humid = " + humid +"%")
		
		f.write(datetime.now().strftime("%Y-%m-%d_%H%M%S") )
		f.write(',')
		f.write(temp)
		f.write(',')
		f.write(humid)
		f.write(',')		
		f.write(str(time.time()))
		f.write('\n')
		f.flush()

		#f.write(datetime.now().strftime("%Y-%m-%d_%H%M%S"), data)
except KeyboardInterrupt: #stop taking data if enter ctrl+c
	pass  

f.close() #save data file
ser.close()
