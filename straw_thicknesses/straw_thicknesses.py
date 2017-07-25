#
#   Author:             Sam Penders
#   Email:         <pende061@umn.edu>
#   Institution: University of Minnesota
#   Project:              Mu2e
#   Date:				7/25/2017
#
#   Description:
#	Program for factory workers to enter straw thickness measurements in. This will save a .csv file
#	of the data, which a manager will upload to the database using master_upload.py.


from datetime import datetime

print 'scan worker ID'
worker_id = raw_input()

print 'scan workstation ID'
workstn_id = raw_input()

print '\nscan straw barcode'
straw = raw_input()

filename = 'straw_thickness_' + datetime.now().strftime("%Y-%m-%d_%H%M%S") + '_' + workstn_id +'.csv'
output = open(filename,"w")

while straw != 'end':
	output.write(straw)
	output.write(',')
	
	output.write( datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
	output.write(',')
	
	print('thickness:')
	thickness = raw_input()
	output.write(thickness)
	output.write(',')
	
	output.write(worker_id)
	output.write(',')
	
	output.write(workstn_id)
	output.write(',\n')
	
	print '\nscan straw barcode (scan end code to stop or type "end")'
	straw = raw_input()
output.close()

#('straw barcode --  batch num -- parent -- worker -- time workstation ID time')
# need workstation id for database

