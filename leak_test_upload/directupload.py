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
		'leak_rate' : round(float(data[5]),7),
		'comments' : str(data[6]),
		'uncertainty' : round(float(data[7]),7),
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
		
# upload leak data after receiving email
def uploadWithEmail(path, date):
	files = [] #put files from certain day into this list
	straws = [] #straw names
	chambers = [] #chamber for each straw
	times = []	
	
	# get list of files with date
	filelist = os.listdir(path)
	for i in filelist:
		if i.endswith(date+ "_rawdata.txt"):
			f = open(path + i)
			files.append(path+i) #make list of files
			straws.append( i[0: i.find('_')])
			line = f.readline();
			data = line.split()
			times.append(str(data[3]) + ' '+ str(data[4])[:-3] )
	
	# fit and upload if files list not empty
	if files != []:
		savefile = 'C:\\Users\\vold\\Desktop\\Mu2e-Factory\\leak_test_upload\\leak_rates\\'+'leak_data_' + date+ '.csv'
		f = open(savefile,'a') 	# file where leak rates get saved
		
		for i in range (0,len(files)):
			fitdata = fit(files[i])
			chambers.append('ch' + str(fitdata[2]))			
			data2upload = straws[i]+','+'co2,wk-spenders01,wsb0001,'+chambers[i]+',' + str(fitdata[0]*10**5)+',,' +str(fitdata[1]*10**5)+','+str(times[i])+'\n'    		
			f.write(data2upload)
			#f.write('%s %s %s %f %s %f %s %s %s' % (straws[i]+',','co2,wk-spenders01,wsb0001,',chambers[i]+',',fitdata[0]*10**5,',,',fitdata[1]*10**5,',',times[i],'\n'))
		f.close()			
		with open(savefile) as readfile:
			file_to_read = csv.reader(readfile)
			for row in file_to_read:
				uploadleaktests(row)
	
		
		
		
