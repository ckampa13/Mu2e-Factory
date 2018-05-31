
import serial
import time
from time import gmtime
import calendar
from datetime import datetime

ser = serial.Serial('/dev/ttyACM0',9600) #port on computer

#filename ='C:\\Users\\vold\\Desktop\\Mu2e-Factory\\temp_humid_sensor\\' + datetime.now().strftime("%Y-%m-%d_%H%M%S")+ '.csv'
filename = 'test.csv'

f = open(filename,"w")
print( 'Hit ctrl+c to quit running arduino and save data')

time.sleep(5)

#send character '5' to arduino
#when arduino gets it, it takes data and sends
f.write('epoch time (s), temp (C), RH (%)\n') 
try:
	while True:
		print("SAM")
		ser.write(b'5')
		time.sleep(4)
		data = str(ser.readline() )
		data = data[:-7]
		data = data[2:]
		f.write( str(calendar.timegm(time.gmtime())))
		f.write(', ')
		f.write(data)
		f.write('\n')
		print(datetime.now().strftime("%Y-%m-%d_%H%M%S"), data)
except KeyboardInterrupt: #stop taking data if enter ctrl+c
	pass  

f.close() #save data file
ser.close()
