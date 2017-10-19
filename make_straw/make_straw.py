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

for i in range (start,end+1):
	n=0
	if i < 10000:
		n = 1
	if i < 1000:
		n = 2
	if i < 100:
		n = 3
	if i < 10:
		n = 4

	output.write('st'+ '0' * n + str(i))
	output.write(',')
	output.write(batchnum)
	output.write(',,') #second comma because not including parent straw at this point
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










