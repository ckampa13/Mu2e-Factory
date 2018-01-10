#
#   Author:             Sam Penders
#   Email:         <pende061@umn.edu>
#   Institution: University of Minnesota
#   Project:              Mu2e
#   Date:				7/25/2017
#
#	Description:
#	python2.7 script to be run by Mu2e factory workers when gluing straws (I'm not sure which epoxying step
#	this refers to, but it corresponds to table "glueups" in test database. Automatic file naming convention
#	is 'glueup_YYYY-MM_DD_HHMMSS_[workstation id].csv" to give files a unique name based on the time. These files will be uploaded to 
#	database by manager based on the day of creation using the master upload program.
#
#	Acceptable glueup types are "first end" and "second end"
#
#	Changes for the future:
#	These currently save onto my machine. Will save to some central location.


from datetime import datetime

print('scan worker ID')
worker_id = input()

print('scan workstation ID')
workstn_id = input()

filename ='glueup_' + datetime.now().strftime("%Y-%m-%d_%H%M%S")+ '_' + workstn_id+ '.csv'
output = open(filename,"w")

print('enter glue batch number:')
batch_num = input()

print('\nscan straw barcode (scan end code to stop or type "end")')
straw = input()

while straw != 'end':
	output.write(straw)
	output.write(',')

	print('scan glueup type')
	glueup_type = input()
	output.write(glueup_type)
	output.write(',')
		
	output.write(worker_id)
	output.write(',')
	
	output.write(workstn_id)
	output.write(',')
	
	print('comments (if any): ')
	comments = input()
	output.write(comments)	
	output.write(',')

	output.write(batch_num)
	output.write(',')

	output.write( datetime.now().strftime("%Y-%m-%d_%H%M%S") )
	output.write('\n')

	print('\nscan straw barcode (scan end code to stop) or type "end"')
	straw = input()
output.close()

