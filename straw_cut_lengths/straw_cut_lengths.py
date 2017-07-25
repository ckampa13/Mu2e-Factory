#
#   Author:             Sam Penders
#   Email:         <pende061@umn.edu>
#   Institution: University of Minnesota
#   Project:              Mu2e
#   Date:				7/25/2017
#
#	Description:
#	python2.7 script to be run by Mu2e factory workers when measuring straw lengths after cutting. Files get 
#	automatically saved as "straw_cut_length_YYYY-MM-DD_HHMMSS.csv." These will be uploaded
#	to Mu2e database by manager using master_upload.py.
#
#	Possible improvements:
#	Change saving to some central location.


from datetime import datetime

print 'scan worker ID'
worker_id = raw_input()

print 'scan workstation ID'
workstn_id = raw_input()

filename ='straw_cut_length_' + datetime.now().strftime("%Y-%m-%d_%H%M%S")+ '_' + workstn_id + '.csv'
output = open(filename,"w")

print '\nscan straw barcode (scan end code to stop or type "end")'
straw = raw_input()
#output.write('\n')
while straw != 'end':
	output.write(straw)
	output.write(',')
	
	output.write( datetime.now().strftime("%Y-%m-%d_%H%M%S") )
	output.write(',')
	
	output.write(worker_id)
	output.write(',')
	
	output.write(workstn_id)
	output.write(',')
	
	print('enter nominal length')
	nom_length = raw_input()
	output.write(nom_length)
	output.write(',')
	
	print('enter measured length')
	measured_length = raw_input()
	output.write(measured_length)
	output.write(',')
	
	print('enter temperature (C)') #will these data fields be automated?
	temp = raw_input()
	output.write(temp)
	output.write(',')
	
	print('enter humidity')
	humidity = raw_input()
	output.write(humidity)
	output.write(',')
	
	print('comments')
	comment = raw_input()
	output.write(comment)
	output.write(',')
	
	output.write('\n')
	print '\nscan straw barcode (scan end code to stop) or type "end"'
	straw = raw_input()
output.close()
