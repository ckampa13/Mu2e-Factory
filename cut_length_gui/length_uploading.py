#made by Sam Penders (pende061@umn.edu) using existing Mu2e database programs
import csv
import os
import time
from DataLoader import DataLoader, DataQuery
from time import strftime
from datetime import datetime

# need to update these 5-2-2018
url = "http://dbweb6.fnal.gov:8080/mu2edev/hdb/loader" #these are the same for all staw tables
queryUrl = "http://dbweb6.fnal.gov:8088/QE/mu2e_hw_dev/app/SQ/query"
group = "Straw Tables"
password = "sdwjmvw"



# change to make actual fields
def createLengthRow(row): # take row of data (in list) as argument
    return{'straw_barcode': str(row[0]),
    #'create_time' : str(row[1]), #Website gets real time somehow.
    'worker_barcode' : str(row[2]),
    'workstation_barcode' : str(row[3]),
    'nominal_length' : str(row[4]),
    'measured_length': str(row[5]),
    'temperature' : str(row[6]),
    'humidity' : str(row[7]),
    #'comments' : str(row[8]),
    }

def uploadLengths(data): # take list of data as argument    
    print(data)
    table = "straw_cut_lengths"
    dataLoader = DataLoader(password,url,group,table)
    dataLoader.addRow(createLengthRow(data))
    retVal,code,text =  dataLoader.send()
    if retVal:
        print "upload" + data[0] + "length success!\n"
        print text
    else:
        print "upload" + data[0] + "length failed!\n"
        print code
        print text
    dataLoader.clearRows()
    
    
##first upload all make_straw files
#def makestraw():

	#def createRow():
		#if str(row[2]) is not '':
			#print str(row[0])
			#return{'straw_barcode': str(row[0]),
			#'batch_number' : str(row[1]),
			##'parent' : str(row[2]),
			#'worker_barcode' : str(row[3]),
			##'create_time' : str(row[4]),
			#}	
		#else: #if there is no parent straw
			#print str(row[0])
			#return{'straw_barcode': str(row[0]),
			#'batch_number' : str(row[1]), 
			#'worker_barcode' : str(row[3]),
			##'create_time' : str(row[4]),
			#}		
	#for row in upload_file:
		##print row
		#createRow()			
		#table = "Straws"
		#dataLoader = DataLoader(password,url,group,table)
		#dataLoader.addRow(createRow())
		#retVal,code,text =  dataLoader.send()

		#if retVal:

			#print "succesfuly made straw " + str(row[0])

		#elif retVal == False:

			#dataLoader = DataLoader(password,url,group,table)
			#aRow = createRow()
			#dataLoader.addRow(aRow,'update')
			#retVal,code,text =  dataLoader.send()

			#if retVal:
				#print "succesfully updated straw " + str(row[0])
		#else:
			#print "fail to make or update straw " + str(row[0])
			#print code

		#dataLoader.clearRows()
