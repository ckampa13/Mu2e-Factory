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
	
	

print("which day to you want to fit leak test data for?")
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
path = "/home/sam/Mu2e-Factory/leak_test_upload/Leak Test Results/"
files = [] #put files from certain day into this list
straws = [] #straw names
chambers = [] #chamber for each straw
times = []


filelist = os.listdir(path)
for i in filelist:
	if i.endswith(date+ "_rawdata.txt"):
		f = open(path + i)
		files.append(path+i) #make list of files
		straws.append( i[0: i.find('_')])
		line = f.readline();
		data = line.split()
		times.append(str(data[3]) + ' '+ str(data[4])[:-3] )

entry = "fsdfsdfsd"		
if files != []:
	for i in range (0,len(files)):
		print(files[i])
else:
	print "No files for today."
	sys.exit()
	
		
entry = raw_input("\nFit and upload these leak test files? (y/n)\n")

if( entry == 'y' ):
	savefile = 'leak_data_' + date+ '.csv'
	f = open(savefile,'w')

	for i in range (0,len(files)):
		fitdata = fit(files[i])
		chambers.append('ch' + str(fitdata[2]))
		#print('%s %f %f' % (straws[i], fitdata[0]*10**5,fitdata[1]*10**5))
		
		data2upload = straws[i]+','+'co2,wk-spenders01,wsb0001,'+chambers[i]+',' + str(fitdata[0]*10**5)+',,'+str(fitdata[1]*10**5)+','+times[i]
		#print(data2upload)
		
		f.write('%s %s %s %f %s %f %s %s %s' % (straws[i]+',','co2,wk-spenders01,wsb0001,',chambers[i]+',' ,fitdata[0]*10**5,',,',fitdata[1]*10**5,',',times[i],'\n'))
	f.close()
		
	with open(savefile) as readfile:
			file_to_read = csv.reader(readfile)
			for row in file_to_read:
				uploadleaktests(row)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
