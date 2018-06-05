# Program to send emails from Mu2e bot to mu2eFactory email
#
# taken from:
# https://avleonov.com/2017/09/14/sending-and-receiving-emails-automatically-in-python/

import datetime
from datetime import date
import csv
import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import matplotlib.pyplot as plt
import numpy as np
import os

# get all files in directory that start with 
# test_type and are on given date
def todayFiles(directory, date, test_type):
	allfiles = os.listdir(directory)
	files = []
	for item in allfiles:
		if( item.startswith(test_type) and item.endswith(date + '.csv')):
			files = files + [item]
	return files

# get hours worked by each worker on each task	
def workerHours(workers, filename):
	#for i in range (0,len(workers)): # change name to all caps
		#workers[i] = workers[i].upper()
	
	index = range(len(workers))
	dictionary = dict(zip(workers,index))
	
	# initialize hours for each worker to zero
	total = [0] * len(workers)
	qc = [0] * len(workers)
	straw = [0] * len(workers)
	panel = [0] * len(workers)
	
	with open(filename) as csvfile:
		data = csv.reader(csvfile,delimiter=',')
		for row in data:
			name = row[0].strip()
			if name in dictionary: # exclude TEST1, etc
				i = dictionary[name]
				total[i] = total[i] + float(row[2])
				qc[i] = qc[i] + float(row[4])
				straw[i] = straw[i] + float(row[6])
				panel[i] = panel[i] + float(row[8])
	return dictionary, total, qc, straw, panel

# get worker names	
def workerNames(filename):
	names = [] # to be returned
	
	with open(filename) as csvfile:
		data = csv.reader(csvfile,delimiter = ',')
		for row in data:
			tempnames = row
	for i in range (0,len(tempnames)):
		tempnames[i] =  tempnames[i].strip()
		if tempnames[i] != '' and tempnames[i].startswith('Test') == False and tempnames[i] != 'TAILNAME':
			names.append(tempnames[i].upper())
	return names

# get weeks, total, qc, straw, panel hours from past five weeks
def hoursHistory(filename):
	week = []
	total = [] # total hrs
	qc = [] # qc hrs etc
	straw = []
	panel = []
	
	with open(filename) as csvfile:
		data = csv.reader(csvfile,delimiter = ',')
		i = 0
		for row in reversed(list(data)):
			if str(row[0]) == 'week' or i == 5:
				break
			week = [int(row[0])] + week
			total = [float(row[1])] + total
			qc = [float(row[2])] + qc
			straw = [float(row[3])] + straw
			panel = [float(row[4])] + panel
			i = i+1
	return week, total, qc, straw, panel

# bar graphs of hours worked on different processes	
def makeBarGraphTotalHrs(current_week, week, total, qc, straw, panel,savefolder):
	plot = plt.bar(week, total)
	plt.xlabel('Week')
	plt.ylabel('Total Hours Worked')
	savename = savefolder + 'week_' + str(current_week) +'_total_history.pdf'
	plt.xticks(week)
	plt.savefig(savename)
	plt.close()
	
	plot = plt.bar(week, qc)
	plt.xlabel('Week')
	plt.ylabel('QC Hours')
	plt.xticks(week)
	savename = savefolder + 'week_' + str(current_week) +'_qc_history.pdf'
	plt.savefig(savename)
	plt.close()
	
	plot = plt.bar(week, straw)
	plt.xlabel('Week')
	plt.ylabel('Straw Hours')
	plt.xticks(week)
	savename = savefolder + 'week_' + str(current_week) +'_straw_history.pdf'
	plt.savefig(savename)
	plt.close()
	
	plot = plt.bar(week, panel)
	plt.xlabel('Week')
	plt.ylabel('Panel Hours')
	plt.xticks(week)
	savename = savefolder + 'week_' + str(current_week) +'_panel_history.pdf'
	plt.savefig(savename)
	plt.close()

# make bar graph of how much each worker worked at each task
# IMPORTANT: this takes the dictionary of worker names and indexes as input
# the total, qc, straws, etc are in same order!	
def makeBarGraphIndividualHours(current_week, workerDict, total, qc, straw, panel,savefolder ):
	workers = sorted(workerDict, key = workerDict.get) 	# sort names by index
	for i in range (0,len(workers)):
		name = workers[i]
		workers[i] = name[0:5] # only show first 5 letters of name
			
	plot = plt.bar(workers, total)
	plt.ylabel('Total Hours Worked')
	plt.xticks(rotation=45)
	savename = savefolder + 'week_' + str(current_week) +'_workers_total.pdf'
	plt.title('Week ' + str(current_week))
	plt.savefig(savename)
	plt.close()
	
	plot = plt.bar(workers, qc)
	plt.ylabel('QC Hours')
	plt.title('Week ' + str(current_week))
	plt.xticks(rotation=45)
	savename = savefolder + 'week_' + str(current_week) +'_workers_qc.pdf'
	plt.savefig(savename)
	plt.close()
	
	plot = plt.bar(workers, straw)
	plt.ylabel('Straw Hours')
	plt.title('Week ' + str(current_week))
	plt.xticks(rotation=45)
	savename = savefolder + 'week_' + str(current_week) +'_workers_straw.pdf'
	plt.savefig(savename)
	plt.close()
	
	plot = plt.bar(workers, panel)
	plt.ylabel('Panel Hours')
	plt.title('Week ' + str(current_week))
	plt.xticks(rotation=45)
	savename = savefolder + 'week_' + str(current_week) +'_workers_panel.pdf'
	plt.savefig(savename)
	plt.close()
 
 # check that individual hours entered match total within an hour   
def hoursAccuracy(total, qc, straw, panel): 
    if( abs( qc + straw + panel - total ) <= 1 ):  
        return True
    else:
        return False

def saveWeeklyHours(week, hours, savefile):
	if os.path.exists(savefile):
		f = open(savefile,'a')
		f.write(str(week)+',')
		for i in range(len(hours)-1):
			f.write("%.1f," % hours[i])
		f.write("%.1f" % hours[3])
		f.write('\n')
	else:
		f = open(savefile,'w')
		f.write('week,total hrs (from punch in/out),QC hrs, straw hrs, panel hrs\n')
		f.write(str(week)+',')
		for i in range(len(hours)-1):
			f.write("%.1f," % hours[i])
		f.write("%.1f" % hours[3])
		f.write('\n')
	f.close()				

# function to send email asking for confirmation
def send_total_hours_worked(directory, hours, week): # directory where data is located
	# sencder info
	login = 'mu2e.bot.umn@gmail.com'
	password = 'Mu2e2021'
	sender = 'mu2e.bot.umn@gmail.com'

	receivers = ['mu2efactory@gmail.com']
	# receivers = ['mu2efactory@gmail.com','pende061@umn.edu','ambrose0028@gmail.com','jason.s.bono@gmail.com','caronj@umn.edu']

	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = ", ".join(receivers)
	msg['Subject'] = 'MU2E FACTORY WEEK ' + str(week) + ' HOURS'
	
	
	# message bodys
	TEXT = "WEEK " + str(week) + " HOURS\n\n"
	
	TEXT = TEXT + "QC    = " + str(hours[1]) + ' hrs\n'
	TEXT = TEXT + "straw = " + str(hours[2])+ ' hrs\n'
	TEXT = TEXT + "panel = " + str(hours[3]) + ' hrs\n'
	TEXT = TEXT + "-----------------------\n"
	TEXT = TEXT + "total   = " + str(round(hours[0],1)) + " hrs (from punch in/punch out time)\n"

	TEXT = TEXT + "\n"
	TEXT = TEXT + "-Mu2e bot"

	msg.attach(MIMEText(TEXT))
	
	# files to attach
	plot1 = directory + 'plots/week_' + str(week) +'_total_history.pdf'
	plot2 = directory + 'plots/week_' + str(week) +'_workers_total.pdf'
	filenames = [plot1, plot2]
	for entry in filenames:
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(entry, 'rb').read())
		encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"'
						% os.path.basename(entry))
		msg.attach(part)

	smtpObj = smtplib.SMTP('smtp.gmail.com:587')
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(login, password)
	smtpObj.sendmail(sender, receivers, msg.as_string())
	
	print("WEEK " + str(week) + " HOURS SENT")		
	return
	
def send_QC_hours(directory, qcHours, week): # directory where data is located
	# sencder info
	login = 'mu2e.bot.umn@gmail.com'
	password = 'Mu2e2021'
	sender = 'mu2e.bot.umn@gmail.com'

	receivers = ['mu2efactory@gmail.com']
	# receivers = ['mu2efactory@gmail.com','pende061@umn.edu','ambrose0028@gmail.com','jason.s.bono@gmail.com','caronj@umn.edu']

	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = ", ".join(receivers)
	msg['Subject'] = 'MU2E FACTORY WEEK ' + str(week) + ' QC HOURS'
	
	
	# message bodys
	TEXT = "WEEK " + str(week) + " HOURS\n\n"
	
	TEXT = TEXT + "total QC hours   = " + str(qcHours) + '\n'
	TEXT = TEXT + "\n"
	TEXT = TEXT + "-Mu2e bot"

	msg.attach(MIMEText(TEXT))
	
	# files to attach
	plot1 = directory + 'plots/week_' + str(week) +'_workers_qc.pdf'
	filenames = [plot1]
	for entry in filenames:
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(entry, 'rb').read())
		encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"'
						% os.path.basename(entry))
		msg.attach(part)

	smtpObj = smtplib.SMTP('smtp.gmail.com:587')
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(login, password)
	smtpObj.sendmail(sender, receivers, msg.as_string())
	
	print("WEEK " + str(week) + " QC HOURS SENT")		
	return
	
def send_straw_hours(directory, strawHours, week): # directory where data is located
	# sencder info
	login = 'mu2e.bot.umn@gmail.com'
	password = 'Mu2e2021'
	sender = 'mu2e.bot.umn@gmail.com'

	receivers = ['mu2efactory@gmail.com']
	# receivers = ['mu2efactory@gmail.com','pende061@umn.edu','ambrose0028@gmail.com','jason.s.bono@gmail.com','caronj@umn.edu']

	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = ", ".join(receivers)
	msg['Subject'] = 'MU2E FACTORY WEEK ' + str(week) + ' STRAW HOURS'
	
	
	# message bodys
	TEXT = "WEEK " + str(week) + " HOURS\n\n"
	
	TEXT = TEXT + "total straw hours   = " + str(strawHours) + '\n'
	TEXT = TEXT + "\n"
	TEXT = TEXT + "-Mu2e bot"

	msg.attach(MIMEText(TEXT))
	
	# files to attach
	plot1 = directory + 'plots/week_' + str(week) +'_workers_straw.pdf'
	filenames = [plot1]
	for entry in filenames:
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(entry, 'rb').read())
		encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"'
						% os.path.basename(entry))
		msg.attach(part)

	smtpObj = smtplib.SMTP('smtp.gmail.com:587')
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(login, password)
	smtpObj.sendmail(sender, receivers, msg.as_string())
	
	print("WEEK " + str(week) + " STRAW HOURS SENT")		
	return
	
def send_panel_hours(directory, panelHours, week): # directory where data is located
	# sencder info
	login = 'mu2e.bot.umn@gmail.com'
	password = 'Mu2e2021'
	sender = 'mu2e.bot.umn@gmail.com'

	receivers = ['mu2efactory@gmail.com']
	# receivers = ['mu2efactory@gmail.com','pende061@umn.edu','ambrose0028@gmail.com','jason.s.bono@gmail.com','caronj@umn.edu']

	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = ", ".join(receivers)
	msg['Subject'] = 'MU2E FACTORY WEEK ' + str(week) + ' PANEL HOURS'
	
	
	# message bodys
	TEXT = "WEEK " + str(week) + " HOURS\n\n"
	
	TEXT = TEXT + "total panel hours   = " + str(panelHours) + '\n'
	TEXT = TEXT + "\n"
	TEXT = TEXT + "-Mu2e bot"

	msg.attach(MIMEText(TEXT))
	
	# files to attach
	plot1 = directory + 'plots/week_' + str(week) +'_workers_panel.pdf'
	filenames = [plot1]
	for entry in filenames:
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(entry, 'rb').read())
		encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"'
						% os.path.basename(entry))
		msg.attach(part)

	smtpObj = smtplib.SMTP('smtp.gmail.com:587')
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(login, password)
	smtpObj.sendmail(sender, receivers, msg.as_string())
	
	print("WEEK " + str(week) + " PANEL HOURS SENT")		
	return

def getHours(data_file): # sum up hours for week
	hours = [0, 0, 0, 0] # total, wc, straw, panel
	with open(data_file) as csvfile:
		data = csv.reader(csvfile, delimiter = ',')
		for row in data: # total up hours
			hours[0] = hours[0] + float(row[2])
			# check that hours entered are reasonable
			if hoursAccuracy( float(row[2]), float(row[4]), float(row[6]), float(row[8])):
				hours[1] = hours[1] + float(row[4]) # qc hrs
				hours[2] = hours[2] + float(row[6]) # straw hrs
				hours[3] = hours[3] + float(row[8]) # panel hrs
				
	# hours[3] = hours[0] + hours[1] + hours[2] # total hours		
	return hours # [QC hrs, ST hrs, PA hrs]


def main(file_directory):
	print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
	print('EMAIL HOURS WORKED PROGRAM RUNNING')
	print('----------------------------------')
	while True:						
		if datetime.datetime.today().weekday() == 2: # check if saturday
			week = datetime.datetime.today().isocalendar()[1] # current week
			workers = workerNames('allowedInputs.txt')
			hours = getHours(file_directory + 'Week_' + str(week))	# hours for this week							
			saveWeeklyHours(week, hours,file_directory+'weekly_hours.csv')
			
			# get data for total hours worker, hours worker by students
			weeks, total, qcTotal, strawTotal, panelTotal = hoursHistory('weekly_hours.csv')
			workerDictionary, worker_total, worker_qc, worker_straw, worker_panel = workerHours(workers,'Week_' + str(week))
			
			# gnerate bar graphs of hours
			makeBarGraphIndividualHours(week, workerDictionary, worker_total, worker_qc, worker_straw, worker_panel,file_directory+'plots/')
			makeBarGraphTotalHrs(week, weeks, total, qcTotal, strawTotal, panelTotal,file_directory+'plots/') # make bar graphs		
			# hours from week worked
			
			send_total_hours_worked(file_directory, hours, week)
			send_QC_hours(file_directory, hours[1], week)
			send_straw_hours(file_directory, hours[2], week)
			send_panel_hours(file_directory, hours[3], week)

		time.sleep(3600*24)
#------------------ for testing ------------------------------			
# main('/home/mu2e/Desktop/Even Newer GUI/')
main('/home/sam/Desktop/email_update/')

workers = workerNames('allowedInputs.txt')
dictionary, total, qc, straw, panel = workerHours(workers,'Week_19')

makeBarGraphIndividualHours(19, dictionary, total, qc, straw, panel,'plots/')





