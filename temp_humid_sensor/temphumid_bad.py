#Initialize serial connection with Arduino and wait for a good connection...will send 'Ready!'

import serial
import time
from time import gmtime
import calendar
from datetime import datetime

ser = serial.Serial('/dev/ttyACM0',9600)

filename ='/home/sam/Mu2e-Factory/temp_humid_sensor/_temp_data_' + datetime.now().strftime("%Y-%m-%d_%H%M%S")+ '.csv'
#filename = 'test.txt'

f = open(filename,"w")
print( 'Hit ctrl+c to quit running arduino and save data')

#time.sleep(1)

f.write('epoch time (s), temp (F), RH (%)\n')
try:
	while True:
		ser.write(b'5')
		time.sleep(1)
		#print(ser.readline())
		data = str(ser.readline())
		print(data)
		#data = data[:-7]
		#data = data[2:]
		f.write( str(calendar.timegm(time.gmtime())))
		f.write(', ')
		f.write(data)
		f.write('\n')
		#i = input()
		#print(data)
except KeyboardInterrupt:
	pass  

f.close()
ser.close()
