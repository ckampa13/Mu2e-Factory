# takes file name as input (full path) and returns array with leak rate as first entry
# and leak rate error as second entry



import logging
import time
import os
import sys
import csv
import msvcrt
from datetime import datetime
#import numpy as np
#import matplotlib.pyplot as plt
from least_square_linear import *

#Change log
#9/15/16
#Fits any raw output file to a linear line

def fit(filename):
#Fit requirements
	excluded_min_time = 200
	excluded_max_time = 7200
	
	#get up-to-date chamber volumes
	volumes_file = "C:\\Users\\vold\\Desktop\\Mu2e-Factory\\leak_chmb_0-24_calibration\\ch0-ch24_chambervolumes.csv"
	chamber_volume = [] 
	chamber_volume_err = []
	with open(volumes_file) as readfile:
		file_to_read = csv.reader(readfile)
		for row in file_to_read:
			chamber_volume.append(float(row[0]))
			chamber_volume_err.append(float(row[1]))

	
	
	
	number_of_chambers = len(chamber_volume)
	straw_volume = 26.0
	for n in range(number_of_chambers) :
			chamber_volume[n] = chamber_volume[n] - straw_volume
	#100% CO2 to argon/CO2
	#(conversion_rate*real_leak_rate=the_leak_rate_when_using_20/80_argon/co2, assuming leak rate is proportional to percentage of co2)
	conversion_rate = 0.14
	#max leak rate for straws
	straws_in_detector = 20736
	total_leak_detector = 6 #cc/min
	max_leakrate = float(total_leak_detector)/float(straws_in_detector)  #CC/min
	max_leakrate = max_leakrate/3

	#dictionary for name of chambers with chamber address in arduino
	"""chamber_id = {}
	for i in range(0,number_of_chambers):
		ch_name = 'ch'+str(i);
		ch_address = i%5 #arduino address
		chamber_id = chamber_id.update( {ch_name : ch_name, ch_address : ch_name} )
	"""
				  
	#filefolder = input("File folder(location from desktop) : ")
	#filename = input("File name (without _rawdata.txt) : ")
	#file = open('C:\\Users\\vold\\Desktop\\' + filefolder + '\\' + filename + '_rawdata.txt',"a+",1)
	#filefolder = 'Leak Test Results'
	#filename = 'st01056_2_chamber16_2018_01_05'
	#file = open(filename,"a+",1)
	
	#get chamber number from filename
	start_num = filename.find("chamber")+7
	end_num = len(filename)-23
	chamber_num = int(filename[start_num:end_num])
	#print(chamber_num)
								
	PPM = {}
	PPM_err = {}
	timestamp = {}
	starttime = []
	slope = []
	slope_err = []
	intercept = []
	intercept_err = []
	for f in range(number_of_chambers):
			PPM[f] = []
			PPM_err[f] = []
			timestamp[f] = []
			starttime.append(0)
			slope.append(0)
			slope_err.append(0)
			intercept.append(0)
			intercept_err.append(0)
			if f == chamber_num :
					#print('Opening file : C:\\Users\\vold\\Desktop\\' + filename + '_rawdata.txt')
					with open(filename,"r+",1) as readfile :
							for line in readfile:
									numbers_float = line.split()[:3]
									if float(numbers_float[2]) < 1 :
											continue
									if starttime[f] == 0 :
											starttime[f] = float(numbers_float[0])
											
									eventtime = float(numbers_float[0]) - starttime[f]
									if eventtime > excluded_min_time :
											if eventtime < excluded_max_time :
													PPM[f].append(float(numbers_float[2]))
													PPM_err[f].append(((float(numbers_float[2])*0.02)**2 + 20**2)**0.5)
													timestamp[f].append(eventtime)
											
							slope[f] = get_slope(timestamp[f], PPM[f], PPM_err[f])
							slope_err[f] = get_slope_err(timestamp[f],PPM[f],PPM_err[f])
							intercept[f] = get_intercept(timestamp[f], PPM[f], PPM_err[f])
							intercept_err[f] = get_intercept_err(timestamp[f],PPM[f],PPM_err[f])
							
							#leak rate in cc/min = slope(PPM/sec) * chamber_volume(cc) * 10^-6(1/PPM) * 60 (sec/min) * conversion_rate
							leak_rate = slope[f]*chamber_volume[f]*(10 ** -6)*60 * conversion_rate 
							#error = sqrt((lr/slope)^2 * slope_err^2 + (lr/ch_vol)^2 * ch_vol_err^2)
							leak_rate_err = ((leak_rate/slope[f])**2 * slope_err[f]**2 + (leak_rate/chamber_volume[f])**2 * chamber_volume_err[f]**2) ** 0.5
									 
							return( leak_rate, leak_rate_err, chamber_num)
						   #Graph and save graph of fit
							"""x = np.linspace(0,max(timestamp[f]))
							y = slope[f]*x + intercept[f]
							plt.plot(timestamp[f],PPM[f],'bo')
							#plt.errorbar(timestamp[f],PPM[f], yerr=PPM_err[f], fmt='o')
							plt.plot(x,y,'r')
							plt.xlabel('time (s)')
							plt.ylabel('CO2 level (PPM)')
							plt.title(filename + '_fit')
							plt.figtext(0.49, 0.80,
									 'Slope = %.2f +- %.2f x $10^{-3}$ PPM/sec \n' % (slope[f]*10**4,slope_err[f]*10**4) +\
									 'Leak Rate = %.2f +- %.2f x $10^{-5}$ cc/min \n' % (leak_rate *(10**5),leak_rate_err*(10**5)),
											 fontsize = 12, color = 'r')
							plt.savefig('C:\\Users\\vold\\Desktop\\' + filefolder + '\\' + filename + '_fit.pdf')
							plt.clf()
							print('success')
							"""


