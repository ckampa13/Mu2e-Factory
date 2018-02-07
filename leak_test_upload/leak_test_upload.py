#
#   Author:             Sam Penders
#   Email:         <pende061@umn.edu>
#   Institution: University of Minnesota
#   Project:              Mu2e
#   Date:				1-08-2018
#
#	Description:
#	python2.7 script which will ask the user to enter a specified date to
#	upload leak test data from. The program will then fit the data from that 
#	date, and upload to the database. 
#	NOTE: straws must already be entered in the database using make_straw.bat
#
#	Possible improvements:
#	Change saving to some central location.



import csv
import os
import time
from DataLoader import DataLoader, DataQuery
from time import strftime
from datetime import datetime
from Run_Fit import fit
import sys

def createRow(data):
		return{'straw_barcode': str(data[0]),
		#'create_time' : str(data[1]), #Website gets real time somehow.
		'test_type' : str(data[1]),
		'worker_barcode' : str(data[2]),
		'workstation_barcode' : str(data[3]),
		#data[4] is channel where it was tested
		'leak_rate' : float(data[5]),
		'comments' : str(data[6]),
		'uncertainty' : float(data[7]),
		'leak_test_timestamp': str(data[8])}

def uploadleaktests(data): #takes string of data as argument
	url = "http://dbweb6.fnal.gov:8080/mu2edev/hdb/loader" #these are the same for all staw tables
	queryUrl = "http://dbweb6.fnal.gov:8088/QE/mu2e_hw_dev/app/SQ/query"
	group = "Straw Tables"
	password = "sdwjmvw"
	table = "Straw_Leak_Tests"
		
	dataLoader = DataLoader(password,url,group,table)
	dataLoader.addRow(createRow(data))
	retVal,code,text =  dataLoader.send()
	if retVal:
		print data[0]+": successful upload"
		print text
	else:
		print data[0]+": failed upload"
		print code
		print text
	dataLoader.clearRows()
	
	

print("\nWhich day to you want to fit leak test data for?")
date = raw_input("Enter 't' for today, or any date in YYYY_MM_DD format\n")
print

proper_date = False
while proper_date == False:
	if date == "t":
		date = datetime.now().strftime("%Y_%m_%d")
		proper_date = True
		
	elif len(date) != 10 or int(date[:4])<2000:
		proper_date = False
		print "\nPlease enter date in correct format."
		date = raw_input("Enter 't' for today, or any date in YYYY_MM_DD format\n")
	else:
		proper_date = True
		
#date = "2018_01_09"	
path = "C:\\Users\\vold\\Desktop\\Leak Test Results\\"
files = [] #put files from certain day into this list
straws = [] #straw names
chambers = [] #chamber for each straw
times = [] #time of test


filelist = os.listdir(path) #read in all files
for i in filelist:
	if i.endswith(date+ "_rawdata.txt"):
		f = open(path + i)
		files.append(path+i) #make list of files
		straws.append( i[0: i.find('_')]) #get straw name
		line = f.readline();
		data = line.split() #get first line of data in file
		times.append(str(data[3]) + ' '+ str(data[4])[:-3]) #get time 

entry = "fsdfsdfsd"		
if files != []:
	for i in range (0,len(files)):
		print(files[i]) #print all files to be uploaded
else:
	print "No files for today."
	sys.exit()
	
		
entry = raw_input("\nFit and upload these leak test files? (y/n)\n")

if( entry == 'y' ):
	savefile = 'leak_data_' + date+ '.csv'
	f = open(savefile,'w')

	for i in range (0,len(files)):
		fitdata = fit(files[i]) #fit all data from specified day
		chambers.append('ch' + str(fitdata[2]))
		#print('%s %f %f' % (straws[i], fitdata[0]*10**5,fitdata[1]*10**5))
		
		data2upload = straws[i]+','+'co2,wk-spenders01,wsb0001,'
		+chambers[i]+',' + str(fitdata[0]*10**5)+',,'+str(fitdata[1]*10**5)+','+times[i]
		#print(data2upload)
		
		f.write(straws[i]+','+'co2,wk-spenders01,wsb0001,'+chambers[i]+
		','+str(fitdata[0])+',,'+str(fitdata[1])+','+times[i]+'\n')
	f.close()
	
	#upload all leak test data	
	with open(savefile) as readfile:
			file_to_read = csv.reader(readfile)
			for row in file_to_read:
				uploadleaktests(row)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
