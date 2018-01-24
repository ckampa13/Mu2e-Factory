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
from sound import * #This contains beep sounds made by computer

#Change log
#9/15/16
#Created to run background tests of the leak test chambers chambers

#Fit requirements
min_number_datapoints = 10  #requires 10 datapoints before attempting to fit
excluded_time = 15 #wait 2 minutes before using data for fit
max_time = 172800 #Max test 2 days
max_co2_level = 1000 # when PPM exceeds 1800 stops fitting and warns user of failure
#calibration volumes from pure CO2 on 9/1/2015
#chamber_volume = [629,609,638,560,567]
#chamber_volume_err = [16,19,14,19,27]
#Estimated volume guess before calibration on 12/20/2017
chamber_volume = [500,500,500,500,500]
chamber_volume_err = [100,100,100,100,100]
number_of_chambers = 5
com = "COM16"

#name of chambers
chamber_id = { "ch45" : 0, "ch46" : 1, "ch47" : 2, "ch48" : 3, "ch49" : 4, 0: "ch45", 1 : "ch46", 2 : "ch47", 3 : "ch48", 4 : "ch49"}
Choosenames = [ "ch45", "ch46", "ch47", "ch48", "ch49" ]
for n in range(number_of_chambers):
        Choosenames[n] = chamber_id[n] + '_background_' + datetime.now().strftime("%Y_%m_%d")
files = {}
 
#Changing file names
def Update_names() :
        for f in range(number_of_chambers):
                filename = 'C:\\Users\\vold\\Desktop\\Background Test Results\\'+Choosenames[f]
                files[f] = open(filename + '_rawdata.txt',"a+",1)
                print('Saving data to file %s' %Choosenames[f])


#Main Code
print ('Begin Background Test' )
print ('Connected to ' + com )
Update_names()

#access Arduino
arduino = serial.Serial(com,115200)

#Main code
pasttime = time.time()
while True:
        #Read arduino and split into multiple files
        ppms = arduino.readline().strip().split()
        formattedList = ["%5.2f" % float(member) for member in ppms]
        currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        epoctime = time.time()
        file = int(float(formattedList[0])) 
        files[file].write(str(epoctime))
        files[file].write(" \t")
        files[file].write("\t".join(formattedList))
        files[file].write("\t" + currenttime)
        files[file].write("\n")
        files[file].flush()

        if epoctime >= (pasttime + 15.0) :
                print("")
                print(com)
                print(currenttime)
                pasttime = epoctime
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
                        with open('C:\\Users\\vold\\Desktop\\Background Test Results\\'+ Choosenames[f] + '_rawdata.txt',"r+",1) as readfile :
                                for line in readfile:
                                        numbers_float = line.split()[:3]
                                        if float(numbers_float[2]) < 1 :
                                                continue
                                        if starttime[f] == 0 :
                                            starttime[f] = float(numbers_float[0])
                                        eventtime = float(numbers_float[0]) - starttime[f]
                                        if eventtime > excluded_time :
                                                PPM[f].append(float(numbers_float[2]))
                                                PPM_err[f].append(((float(numbers_float[2])*0.02)**2 + 20**2)**0.5)
                                                timestamp[f].append(eventtime)
                                if len(PPM[f]) < 2 :
                                        print("Chamber %s not connected" % chamber_id[f])
                                        continue
                                if max(PPM[f]) > max_co2_level :
                                        print("CO2 in chamber %s exceeds 1000. Please flush chamber" % chamber_id[f])
                                        continue
                                if max(timestamp[f]) > max_time :
                                        print("%s has been in Chamber %s for over 2 Days. Data is saving but no longer fitting." %(Choosenames[f][:7],chamber_id[f]))
                                        continue
                                slope[f] = get_slope(timestamp[f], PPM[f], PPM_err[f])
                                slope_err[f] = get_slope_err(timestamp[f],PPM[f],PPM_err[f])
                                intercept[f] = get_intercept(timestamp[f], PPM[f], PPM_err[f])
                                intercept_err[f] = get_intercept_err(timestamp[f],PPM[f],PPM_err[f])
                                straw_status = "unknown status"
                                print("Background rate in chamber %s is %.2f +- %.2f PPM per hour" % (chamber_id[f],slope[f]*3600,slope_err[f]*3600))

                                #Graph and save graph of fit
                                x = np.linspace(0,max(timestamp[f]))
                                y = slope[f]*x + intercept[f]
                                plt.plot(timestamp[f],PPM[f],'bo')
                                #plt.errorbar(timestamp[f],PPM[f], yerr=PPM_err[f], fmt='o')
                                plt.plot(x,y,'r')
                                plt.xlabel('time (s)')
                                plt.ylabel('CO2 level (PPM)')
                                plt.title(Choosenames[f] + '_fit')
                                plt.figtext(0.49, 0.80,
                                         'Slope = %.2f +- %.2f PPM/hour \n' % (slope[f]*3600,slope_err[f]*3600) +\
                                         straw_status+"\t"+currenttime,
                                         fontsize = 12, color = 'r')
                                plt.savefig('C:\\Users\\vold\\Desktop\\Background Test Results\\'+ Choosenames[f] + '_fit.pdf')
                                plt.clf()


for f in range(number_of_chambers):
        files[f].close()





