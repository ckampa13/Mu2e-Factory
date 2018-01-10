import logging
import time
import serial
import os
import sys
import msvcrt
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from least_square_linear import *
from time import strftime

#Change log
#9/15/16
#Fits any raw output file to a linear line

#Fit requirements
excluded_min_time = 300
excluded_max_time = 3600
chamber_volume = [629,609,638,560,567,533,489,499,500,422]
chamber_volume_err = [16,19,14,19,27,16,12,12,50,19]
number_of_chambers = 10
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

#name of chambers
chamber_id = {"ch0" : 0, "ch1" : 1, "ch2" : 2, "ch3" : 3, "ch4" : 4,  "ch5" : 5, "ch6" : 6, "ch7" : 7, "ch8" : 8, "ch9" : 9,
		  0 : "ch0", 1 : "ch1", 2 : "ch2", 3 : "ch3", 4 : "ch4", 5 : "ch5", 6 : "ch6", 7 : "ch7", 8 : "ch8", 9 : "ch9"} 
filefolder = ''

filenameoutput = 'C:\\Users\\vold\\Desktop\\Leak Test Results\\leak_test_all.csv'
output = open(filenameoutput,"w") #write all leak rates to file

make_straw = 'C:\\Users\\vold\\Desktop\\Leak Test Results\\make_straw_all.csv'
mk_straw = open(make_straw,"w") #make file to initially create straw in Mu2e hardware database

failed_straw = 'C:\\Users\\vold\\Desktop\\Leak Test Results\\failed_straws.csv'
failed_st = open(failed_straw,"w") #write failed straws to file

#--------------- look for raw data files in folder
path = 'C:\\Users\\vold\\Desktop\\Leak Test Results\\'
filelist = os.listdir(path)
fileend = 'rawdata.txt'
			

for i in filelist:

	PPM = {}
	PPM_err = {}
	timestamp = {}
	starttime = []
	slope = []
	slope_err = []
	intercept = []
	intercept_err = []

	#if i.endswith(fileend) and not i.startswith('empty') and not i.startswith('EMPTY') and not i.endswith('badrawdata.txt'):
	if i.endswith(fileend) and (i.startswith('st006') or i.startswith('st007') or i.startswith('st008')) and not i.endswith('badrawdata.txt'):
			file = open(path + i) #just name of total path
			filename = path + i
	##                print(filename)
			chamber_num = int(str(filename[filename.find('chamber')+7])) #get chamber number from file name
			straw = i[0:int(str(i.find('_chamber')))]

			#print(filename,' ',chamber_num, straw)
			
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
					#print(filename)
					with open(filename,"r+",1) as readfile :
							for line in readfile:
									#print(line)
									numbers_float = line.split()[:3]

						#if (straw == 'st00446'):
								#print(numbers_float)

	
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
							
							if slope[f] != 0:
									leak_rate_err = ((leak_rate/slope[f])**2 * slope_err[f]**2 + (leak_rate/chamber_volume[f])**2 * chamber_volume_err[f]**2) ** 0.5
							else:
									leak_rate_err = 100000000000
							#print(straw,chamber_num, straw,leak_rate,leak_rate_err)


							   #no need to make plots
							if timestamp[f] != []:
									x = np.linspace(0,max(timestamp[f]))
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
									plt.savefig('C:\\Users\\vold\\Desktop\\Leak Test Results\\refits\\' + straw + '.pdf')
									plt.clf()
									print(straw,': success!')
									#print('success')

							#write leak rate data
							output.write(straw)
							output.write(',')
							output.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(numbers_float[0]))) )
							output.write(',')
							output.write('co2,')
							output.write('wb0001,')
							output.write('wsb0001,')
							output.write('ch'+str(chamber_num))
							output.write(',')
							output.write(str(leak_rate))
							output.write(',')
							output.write(str(leak_rate_err))
							output.write('\n')

							#write make_straw file
							batch_nbm = str(123)
							parent_straw = ''
							worker_id_ = 'wk-spenders01'
							mk_straw.write(straw)
							mk_straw.write(',')
							mk_straw.write(batch_nbm)
							mk_straw.write(',,')
							mk_straw.write(worker_id_)
							mk_straw.write(',')
							mk_straw.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(numbers_float[0]))) )
							mk_straw.write('\n')
							
							#if straw 1 number previous doesn't exist, assume it failed
							#if temp_straw != 'st' + 
							
							#write failed straws to file
							if leak_rate > 9*10^-5:
									output.write(straw)
									output.write(',')
									output.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(numbers_float[0]))) )
									failed_st.write(',')
									failed_st.write('co2,')
									failed_st.write('wb0001,')
									failed_st.write('wsb0001,')
									failed_st.write('ch'+str(chamber_num))
									failed_st.write(',')
									failed_st.write(str(leak_rate))
									failed_st.write(',')
									failed_st.write(str(leak_rate_err))
									failed_st.write('\n')
									
							temp_straw = straw
output.close()
mk_straw.close()
failed_st.close()
							




