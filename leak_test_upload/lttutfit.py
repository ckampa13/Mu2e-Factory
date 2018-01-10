import logging
import time
import serial
import os
import sys
import msvcrt
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from least_square_linear import *

#Change log
#9/15/16
#Fits any raw output file to a linear line

#Fit requirements
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
#filefolder = input("File folder(location from desktop) : ")
#filename = input("File name (without _rawdata.txt) : ")
#file = open('C:\\Users\\vold\\Desktop\\' + filefolder + '\\' + filename + '_rawdata.txt',"a+",1)


filefolder = 'Leak Test Results'
                
                
PPM = {}
PPM_err = {}
timestamp = {}
starttime = []
slope = []
slope_err = []
intercept = []
intercept_err = []
I = []

for x in range (1,6):
        filename = 'lttut' + str(x) + '_chamber' + str(x-6) + '_2017_09_01'

        file = open('C:\\Users\\vold\\Desktop\\' + filefolder + '\\' + filename + '_rawdata.txt',"a+",1)
        chamber_num = x-1
	
        for y in range (1,3):
	
                if y == 1:
                        excluded_min_time = 1000
                        excluded_max_time = 10000
                        savename = 'C:\\Users\\vold\\Desktop\\lttutfits\\' + filename + '_1000-10000_fit.pdf'
                if y == 2:
                        excluded_min_time = 15000
                        excluded_max_time = 40000
                        savename = 'C:\\Users\\vold\\Desktop\\lttutfits\\' + filename + '_15000-40000_fit.pdf'				
					


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
                                print('Opening file : C:\\Users\\vold\\Desktop\\' + filefolder + '\\' + filename + '_rawdata.txt')
                                a = open('C:\\Users\\vold\\Desktop\\' + filefolder + '\\' + filename + '_rawdata.txt',"r+",1)
                                with a as readfile :
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
                                        leak_rate_err = ((leak_rate/slope[f])**2 * slope_err[f]**2 +
                                                 (leak_rate/chamber_volume[f])**2 * chamber_volume_err[f]**2) ** 0.5

                                       #Graph and save graph of fit

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
                                                plt.savefig(savename)
                                                plt.clf()
                                                print('success')

#i = 2
#print('1,')
#for j in range(0,20):
 #       print(I[j],',')
  #      if (j+1)%4 ==0:
   #             print('\n')
    #            print(i,',')
     #           i = i+1
        



        
