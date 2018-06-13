# Program to send emails from Mu2e bot to mu2eFactory email
#
# taken from:
# https://avleonov.com/2017/09/14/sending-and-receiving-emails-automatically-in-python/


import datetime
from datetime import date

import matplotlib.pyplot as plt
import numpy as np

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from Run_Fit import fit
import os

# get all files in directory that start with 
# test_type and are on given date
def todayFiles(directory, date):
	allfiles = os.listdir(directory)
	files = []
	for item in allfiles:
		if(item.endswith(date + '_rawdata.txt')):                       
			files = files + [item]
	return files

# make histogram of leakrates from date
def leakHist(data, date):
        plt.hist(data,bins = 30, range = [0, 30])
        plt.title('Leak Rates ' + date)
        plt.xlabel('Leak Rate (10^-5 CC/min)')
        plt.ylabel('Frequency')
        savename = 'C:\\Users\\vold\\Desktop\\Mu2e-Factory\\leak_test_upload\\leak_histograms\\' + 'leakrate_' + date + '.pdf'
        plt.savefig(savename)
        return savename

# put in leak rate data and get number that passed
def numPassed(data):
        passed = 0
        for value in data:
                if value < 9.6: # 9.6 CC/min
                        passed = passed+1
        return passed                              

# function to send email asking for confirmation
def ask2upload(directory, day2upload, receivers):
	# sencder info
	login = 'mu2e.bot.umn@gmail.com'
	password = 'Mu2e2021'
	sender = 'mu2e.bot.umn@gmail.com'

	# receivers
	#receivers = ['mu2efactory@gmail.com','ambrose0028@gmail.com','pende061@umn.edu']
	
	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = ", ".join(receivers)
	msg['Subject'] = day2upload + ' DATA UPLOAD'
	
	# get relevant files
	files2upload = todayFiles(directory, day2upload)
	
	# make histogram of leakrates
	leakrates = []
	for filename in files2upload:
		rate = fit(directory + filename)
		rate = rate[0]*10**5
		leakrates.append(rate)
	attached_hist = leakHist(leakrates, day2upload)

	# leak testing statistics from day
	total_straws = len(leakrates)
	passed = numPassed(leakrates)
	failed = total_straws - passed
	
	# message body
	TEXT = str(day2upload) + '\n' #"Hello,\n"
	TEXT = TEXT + "\n"
	TEXT = TEXT + "These files from " + day2upload + " have not yet been uploaded to the Mu2e database:\n\n"
	
	for filename in files2upload:
		TEXT = TEXT + filename + '\n'
	TEXT = TEXT + "\nTotal tested = " + str(total_straws)
	
	if total_straws != 0:
		TEXT = TEXT + "\nPassed = " + str(passed) +' (' + str(round(passed*100.0/total_straws,1)) + '%)'
		TEXT = TEXT + "\nFailed = " + str(failed) +' (' + str(round(failed*100.0/total_straws,1)) + '%)'	
	TEXT = TEXT + "\n\nReply with a blank email to upload them.\n"
	TEXT = TEXT + "\n"
	TEXT = TEXT + "-Mu2e bot"

	msg.attach(MIMEText(TEXT))

	# files to attach
	filenames = [attached_hist]
	for file in filenames:
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(file, 'rb').read())
		encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"'
						%os.path.basename(file))
		msg.attach(part)

	smtpObj = smtplib.SMTP('smtp.gmail.com:587')
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(login, password)
	smtpObj.sendmail(sender, receivers, msg.as_string())
	
	return

#ask2upload('C:\\Users\\vold\\Desktop\\Leak Test Results\\','2017_09_25')	
			
			
			
