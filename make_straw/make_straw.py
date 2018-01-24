#!C:\Python27\python27

#   Author:             Sam Penders
#   Email:         <pende061@umn.edu>
#   Institution: University of Minnesota
#   Project:              Mu2e
#   Date:				1/8/2018
#
#   Description:
#	A python2.7 script for workers to create a .csv file containing the barcode of a newly made straws, 
#	their batch numbers, and their parent straw barcodes (if applicable). The file is saved as
# 	"make_straw_YYYY-MM-DD_HHMMSS_[workstation id].csv." This precise naming will ensure that if multiple stations
#	are making these files, the filenames will be unique. These files will get uploaded to database by master_upload.py
#	by manager at end of day.
#	
#	Possible changes forthcoming:
#	Assumption was made that all straws would have the same batch number. 
#	The script could be changed to ask the user to enter batch number for every
#	straw, or there could be a prompt to change the batch number. The files should be
#	saved to a central location.
#! c:\Python27\python27.exe

from datetime import datetime
<<<<<<< HEAD

print 'scan worker ID'
worker_id = raw_input()
print 'scan workstation ID'
workstn_id = raw_input()
print 'scan batch number'
batchnum = raw_input()
print '\nscan first straw barcode (lowest number)'
straw1 = raw_input()
print '\nscan last straw barcode (highest number)'
straw2 = raw_input()

filename ='C:\\Users\\vold\\Desktop\\straw_database\\make_straw_' + datetime.now().strftime("%Y-%m-%d_%H%M%S")+'_' + workstn_id + '.csv'
output = open(filename,"w")

start = int(straw1[2:])
end = int(straw2[2:])

=======
from DataLoader import DataLoader, DataQuery
import csv

def createRow(data):
	if str(data[2]) is not '':
		#print str(data[0])
		return{'straw_barcode': str(data[0]),
		'batch_number' : str(data[1]),
		#'parent' : str(data[2]),
		'worker_barcode' : str(data[3]),
		#'create_time' : str(data[4]),
		}	
	else: #if there is no parent straw
		#print str(data[0])
		return{'straw_barcode': str(data[0]),
		'batch_number' : str(data[1]), 
		'worker_barcode' : str(data[3]),
		#'create_time' : str(data[4]),
		}

def upload(data_file):
	table = "Straws"
	url = "http://dbweb6.fnal.gov:8080/mu2edev/hdb/loader"
	#url = "http://rexdb02.fnal.gov:8500/swhite/HdbHandler.py/loader"
	queryUrl = "http://dbweb6.fnal.gov:8088/QE/mu2e_hw_dev/app/SQ/query"
	group = "Straw Tables"
	password = "sdwjmvw"

	with open(data_file) as file_input:
		reader = csv.reader(file_input)
		for row in reader:
			dataLoader = DataLoader(password,url,group,table)
			dataLoader.addRow(createRow(row))
			retVal,code,text =  dataLoader.send()
	
			if retVal:
				print(str(row[0])+" successful upload")
				print(text)
			else:
				print (str(row[0])+ "FAILED upload")
				print(code)
				print(text)

			dataLoader.clearRows()


correct_straws = False

while correct_straws == False:
	print('\nscan worker ID--must be your real ID (e.g. "wk-spenders01")')
	worker_id = raw_input()
	#print('scan workstation ID (e.g. "wsb0001")')
	#workstn_id = raw_input()
	workstn_id = "wsb0001" #temporarily set to default value
	print('\nscan batch number (e.g. "5 12-15-17")')
	batchnum = raw_input()
	print('\nscan first straw barcode (lowest number)')
	straw1 = raw_input()
	print('\nscan last straw barcode (highest number)')
	straw2 = raw_input()
	print('\n')

	filename ='make_straw_' + datetime.now().strftime("%Y-%m-%d_%H%M%S")+'_' + workstn_id + '.csv'
	output = open(filename,"w")

	start = int(straw1[2:])
	end = int(straw2[2:])
	
	for i in range (start,end+1):
		
		if( i == start):
			straw_name = []
			
		n=0
		if i < 10000:
			n = 1
		if i < 1000:
			n = 2
		if i < 100:
			n = 3
		if i < 10:
			n = 4		
		
		straw_name.append('st'+ '0' * n + str(i) )
		

		input_in = False
		if( i == end):
			while input_in == False:
				
				print('Straws to be uploaded:')
				for i in range (start,end+1):
					print( straw_name[i-start] )
				print('%s %s' % ('\nworker id: ', worker_id) )
				#print('%s %s' % ('workstation id: ', workstn_id) )
				print('%s %s' % ('batchnumber: ', batchnum) )

				
				answer = raw_input("\nIs this the correct information? (y/n) \n")
				if answer == 'y':
					correct_straws = True
					input_in = True
				elif answer == 'n':
					correct_straws = False
					input_in = True
				else:
					input_in = False
	
>>>>>>> 4200f5ff179bdd039f7f5afeab69bcc4ed327bfa
for i in range (start,end+1):
	output.write(straw_name[i-start] )
	output.write(',')
	output.write(batchnum)
	output.write(', ,') #second comma because not including parent straw at this point
	#print 'scan parent barcode (if applicable)'
	#parent = raw_input()
	#output.write( parent)
	#output.write(',')
	output.write(worker_id)
	output.write(',')
	output.write( datetime.now().strftime("%Y-%m-%d_%H%M%S") )
	output.write('\n')
output.close()

#('straw barcode --  batch num -- parent -- worker -- time workstation ID time')
# need workstation id for database


upload(filename)







