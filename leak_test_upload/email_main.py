# program that sends emails asking for confirmation, and uploads data when confirmatin
# email is received. Works as of 4/10/2018. -SP


from check_email import check_for_confirmation
from send_email import todayFiles, ask2upload, leakHist
from directupload import createRow, uploadleaktests, uploadWithEmail

import sys
import imaplib
import getpass
import email
import email.header
import datetime
import time

def updateDateToUpload(filename,old_dates,dates2remove):
	new_dates = list(set(old_dates) - set(dates2remove))
	new_dates = sorted(new_dates, key=lambda d: map(int, d.split('_')))

	f = open(filename,'w')
	for date in new_dates:
		f.write(date+'\n')
	f.close()
	return

# account info
EMAIL_ACCOUNT = "mu2e.bot.umn@gmail.com"
PASSWORD = 'Mu2e2021'
EMAIL_FOLDER = "inbox"

M = imaplib.IMAP4_SSL('imap.gmail.com')

# try to login
try:
	rv, data = M.login(EMAIL_ACCOUNT, PASSWORD) #getpass.getpass())
except imaplib.IMAP4.error:
	print("LOGIN FAILED!!! ")
	sys.exit(1)

# print( rv, data )

# list mailboxes
rv, mailboxes = M.list()
rv, data = M.select(EMAIL_FOLDER)

print('\nData upload program running\n')
a = True 
while a == True: # run program indefinitely    
	now = datetime.datetime.now()
	#now = datetime.datetime(2018 ,5, 11, 8, 0, 5)
	#yesterday = datetime.datetime(2018 ,5,10).strftime("%Y_%m_%d")
	#print(yesterday)
		
	yesterday = datetime.date.today()- datetime.timedelta(1)
	yesterday = yesterday.strftime("%Y_%m_%d")
	midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
	minutes_since = (now - midnight).seconds / 60 # minutes since midnight

	datefile = 'C:\\Users\\vold\Desktop\\Mu2e-Factory\\leak_test_upload\\days_not_uploaded\\' + 'dates_not_uploaded.txt'


	# send email during time window in morning (8am)
	if (minutes_since >= 480 and minutes_since <= 545):
		print( str(now.strftime("%Y_%m_%d")) + ': sending leak data email\n')
		f = open(datefile,'a')
		ask2upload('C:\\Users\\vold\\Desktop\\LeakTestGUI - Current Version\\Leak Test Results\\',str(yesterday))
		#ask2upload('C:\\Users\\vold\\Desktop\\Leak Test Results\\',str(yesterday))
		f.write(str(yesterday)+'\n') # add yesterday's date to not uploaded list
		f.close()
		time.sleep(5)
		
	# check email for confirmation during time window, around 8pm	
	if (minutes_since >= 629 and minutes_since <= 645):
		dates_not_uploaded = open(datefile,'r').read().splitlines()
		dates_not_uploaded.append(str(yesterday))
		confirmed_dates = []
		
		if rv == 'OK':
			print(str(now) + ": Checking for confirmation emails...\n")
			for date in dates_not_uploaded:
				if check_for_confirmation(M, date):
					print( 'CONFIRMATION RECEIVED' )
					uploadWithEmail('C:\\Users\\vold\\Desktop\\LeakTestGUI - Current Version\\Leak Test Results\\', str(yesterday))
					confirmed_dates.append(date)
			M.close()
		else:
			print( "ERROR: Unable to open mailbox ", rv )
		updateDateToUpload(datefile,dates_not_uploaded,confirmed_dates)
		time.sleep(5)
		
	time.sleep(3600)   
M.logout()

#           TESTING FUNCTIONS

##yesterday = datetime.date.today()- datetime.timedelta(1)
##yesterday = yesterday.strftime("%Y_%m_%d")
##yesterday = str(yesterday)
##print(yesterday)

#print(check_for_confirmation(M, yesterday))
#ask2upload('C:\\Users\\vold\\Desktop\\LeakTestGUI - Current Version\Leak Test Results\\',str(yesterday))
#uploadWithEmail('C:\\Users\\vold\\Desktop\\LeakTestGUI - Current Version\Leak Test Results\\', str(yesterday))

#yesterday = '2017_07_27'
#ask2upload('C:\\Users\\vold\\Desktop\\Leak Test Results\\',yesterday)
#print(check_for_confirmation(M, yesterday))
#uploadWithEmail('C:\\Users\\vold\\Desktop\\Leak Test Results\\','17_07_27')

#yesterday = '2018_01_09'
#ask2upload('C:\\Users\\vold\\Desktop\\Mu2e-Factory\\leak_test_upload\\test_data\\',yesterday)
#print(check_for_confirmation(M, yesterday))
#uploadWithEmail('C:\\Users\\vold\\Desktop\\Mu2e-Factory\\leak_test_upload\\test_data\\',yesterday)



