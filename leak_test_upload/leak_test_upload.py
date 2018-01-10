import csv
import os
import time
#from DataLoader import DataLoader, DataQuery
from time import strftime
from datetime import datetime
from Run_Fit import fit

print("which day to you want to fit leak test data for?")
date = raw_input("Enter 'today' for today, or any date in YYYY_MM_DD format\n")

if date == "today":
	date = datetime.now().strftime("%Y_%m_%d")
#	print(date,"\n")


date = "2018_01_09"	
#upload leak test data
path = "/home/sam/Mu2e-Factory/leak_test_upload/Leak Test Results/"
files = [] #put files from certain day into this list
straws = []
filelist = os.listdir(path)
for i in filelist:
	#print(i)
	#print(date+ "_rawdata.txt\n")
	if i.endswith(date+ "_rawdata.txt"):
		#f = open(path + i)
		files.append(path+i) #make list of files
		straws.append( i[0: i.find('_')])
		#print path + i
		#upload_file = csv.reader(f)
		#uploadleaktests()
		#f.close()

for i in range (0,len(files)):
	print(files[i])
	
entry = raw_input("Fit and upload these leak test files? (y/n)\n")
print('\n')

savefile = 'leak_data_' + date+ '.csv'
f = open(savefile,'w')

if( entry == 'y' ):
	for i in range (0,len(files)):
		leakrate = fit(files[i])
		print('%s %f %f' % (straws[i], leakrate[0]*10**5,leakrate[1]*10**5))
		f.write('%s %f %s %f %s' % (straws[i]+',', leakrate[0]*10**5, ',' ,leakrate[1]*10**5,'\n'))
