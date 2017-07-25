#
#   Author:             Sam Penders
#   Email:         <pende061@umn.edu>
#   Institution: University of Minnesota
#   Project:              Mu2e
#   Date:				7/25/2017
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



from datetime import datetime

print 'scan worker ID'
worker_id = raw_input()
print 'scan workstation ID'
workstn_id = raw_input()
print 'enter batch number'
batchnum = raw_input()
print '\nscan straw barcode (scan end code to stop or type "end")'
straw = raw_input()

filename ='make_straw_' + datetime.now().strftime("%Y-%m-%d_%H%M%S")+'_' + workstn_id + '.csv'
output = open(filename,"w")

while straw != 'end':
	output.write(straw)
	output.write(',')
	output.write(batchnum)
	output.write(',')
	print 'scan parent barcode (if applicable)'
	parent = raw_input()
	output.write( parent)
	output.write(',')
	output.write(worker_id)
	output.write(',')
	output.write( datetime.now().strftime("%Y-%m-%d_%H%M%S") )
	output.write('\n')
	print '\nscan straw barcode (scan end code to stop) or type "end"'
	straw = raw_input()
output.close()

#('straw barcode --  batch num -- parent -- worker -- time workstation ID time')
# need workstation id for database
