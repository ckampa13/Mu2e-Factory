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
#7/21/17
#accounted for straw volume and plastic tube volume
#Added PPM_max cut of 1800, time max cut of 2 hours, requires 10 datapoints, ignores first 2 minutes measurements
#Filename inludes date, creates new file each day
# 9/15/16  FIXED bug where we were using old 50/50 Argon/CO2 conversion (data was 2 times higher then it should have been)
# 9/15/16  Put in new detector volumes, ch8 not measured yet.

#Fit requirements
min_number_datapoints = 10  #requires 10 datapoints before attempting to fit
excluded_time = 15 #wait 2 minutes before using data for fit
max_time = 7200 #When time exceeds 2 hours stops fitting data (still saving it)
max_co2_level = 1800 # when PPM exceeds 1800 stops fitting and warns user of failure
#calibration volumes from pure CO2 on 9/1/2015
chamber_volume = [594,607,595,605,595]
chamber_volume_err = [9,20,10,6,14]
number_of_chambers = 5
straw_volume = 26.0
for n in range(number_of_chambers) :
        chamber_volume[n] = chamber_volume[n] - straw_volume
#(conversion_rate*real_leak_rate=the_leak_rate_when_using_20/80_argon/co2 in chamber)
#Conversion rate proportional to amount of CO2 (1/5)
#Partial pressure of CO2 as 2 absolution ATM presure inside and 0 outside, chamber will be 1 to 0(1/2)
#Multiplied by 1.4 for the argon gas leaking as well conservative estimate (should we reduce?
conversion_rate = 0.14
#max leak rate for straws
straws_in_detector = 20736
total_leak_detector = 6 #cc/min
max_leakrate = float(total_leak_detector)/float(straws_in_detector)  #CC/min
max_leakrate = max_leakrate/3

#name of chambers
chamber_id = { "ch0" : 0, "ch1" : 1, "ch2" : 2, "ch3" : 3, "ch4" : 4 } 
Choosenames = [ "empty0", "empty1", "empty2", "empty3", "empty4" ]
files = {}
#create a csv file to store leak test results
result = open('C:\\Users\\vold\\Desktop\\Leak Test Results\\' + datetime.now().strftime("%Y-%m-%d_%H%M%S") + '_COM11.csv', "a+",1)
#list of passed straws
straw_list=[]
#changing straws
def Change_straws() :
        chamber_input = False
        this_chamber = 5
        while not chamber_input :
                chamber = input("Scan chamber ")
                for i in chamber_id :
                        if i == chamber :
                                this_chamber = chamber_id[i]
                                print("Chamber is %s" % chamber_id[chamber])
                                chamber_input = True
                                break
                else :
                        print("not a valid Chamber")
        straw = input("Scan straw ")
        if straw == "empty" : #empty chamber
                straw = "empty%s" % this_chamber
                Choosenames[this_chamber] = straw
        else:
                Choosenames[this_chamber] = straw + '_chamber%.0f_' % this_chamber + datetime.now().strftime("%Y_%m_%d") 
        print(straw)
        Need_for_change()
#Do we want to change straws
def Need_for_change() :
        print("Enter anykey to change straws")
        endtime = time.time() + 3.0
        timesup = False
        while not timesup :
                if msvcrt.kbhit():
                        Change_straws()
                        break
                if time.time() > endtime :
                        #print("Returning to data taking")
                        timesup = True
        return not timesup
 
#Changing file names
def Update_names() :
        for f in range(number_of_chambers):
                filename = 'C:\\Users\\vold\\Desktop\\Leak Test Results\\'+Choosenames[f]
                files[f] = open(filename + '_rawdata.txt',"a+",1)
                print('Saving data to file %s' %Choosenames[f])


#Main Code
print ('Connected to port 4' )
Need_for_change()
Update_names()

#access Arduino
arduino = serial.Serial("COM11",115200)

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
                print("COM11")
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
                        with open('C:\\Users\\vold\\Desktop\\Leak Test Results\\'+ Choosenames[f] + '_rawdata.txt',"r+",1) as readfile :
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
                                if (str(Choosenames[f])[0:5] == "empty") :
                                        print("No straw in chamber %.0f" % f)
                                        continue
                                if len(PPM[f]) < min_number_datapoints :
                                        print("Straw %s in chamber %.0f is in preperation stage. Please wait for more data" %(Choosenames[f][:7],f))
                                        #time.sleep(5)
                                        continue
                                if max(PPM[f]) > max_co2_level :
                                        print("CO2 in chamber %.0f exceed 1800. Significant leak?!? Please flush and remove straw" %f)
                                        #time.sleep(5)
                                        #failed()
                                        continue
                                if max(timestamp[f]) > max_time :
                                        print("Straw %s has been in Chamber %.0f for over 2 hours.  Data is saving but no longer fitting." %(Choosenames[f][:7],f))
                                        #time.sleep(5)
                                        continue
                                slope[f] = get_slope(timestamp[f], PPM[f], PPM_err[f])
                                slope_err[f] = get_slope_err(timestamp[f],PPM[f],PPM_err[f])
                                intercept[f] = get_intercept(timestamp[f], PPM[f], PPM_err[f])
                                intercept_err[f] = get_intercept_err(timestamp[f],PPM[f],PPM_err[f])
                                #leak rate in cc/min = slope(PPM/sec) * chamber_volume(cc) * 10^-6(1/PPM) * 60 (sec/min) * conversion_rate
                                leak_rate = slope[f]*chamber_volume[f]*(10 ** -6)*60 * conversion_rate 
                                #error = sqrt((lr/slope)^2 * slope_err^2 + (lr/ch_vol)^2 * ch_vol_err^2)
                                leak_rate_err = ((leak_rate/slope[f])**2 * slope_err[f]**2 +
                                         (leak_rate/chamber_volume[f])**2 * chamber_volume_err[f]**2) ** 0.5
                                straw_status = "unknown status"
                                print("Leak rate for straw %s in chamber %.0f is %.2f +- %.2f CC per minute * 10^-5" % (Choosenames[f][:7],f,leak_rate *(10**5),leak_rate_err*(10**5)))
                                if len(PPM[f]) > 20 and leak_rate < max_leakrate and leak_rate_err < max_leakrate/10:
                                        print("Straw in chamber %.0f has Passed, Please remove" % f)
                                        straw_status = "Passed leak requirement"
                                        #passed()
                                        #save to csv file
                                        if Choosenames[f][:7] in straw_list:
                                                break
                                        else:
                                                print("Enter anykey then go to saving data procedure:")
                                                endtime = time.time() + 1.5
                                                while True:
                                                        if msvcrt.kbhit():
                                                                c = input("save data for this straw?(y/n):")
                                                                straw_list.append(Choosenames[f][:7])
                                                                if c == 'y' or c == 'Y':
                                                                        result.write(Choosenames[f][:7] + ",")
                                                                        result.write(currenttime + ",")
                                                                        result.write("CO2"+",")
                                                                        result.write("wb0001"+",")
                                                                        result.write("ch" + str(f) + ",")
                                                                        result.write(str(leak_rate) + ",")
                                                                        result.write(str(leak_rate_err) + "\n")
                                                                break
                                                        if time.time() > endtime:
                                                                break
                                if len(PPM[f]) > 20 and leak_rate > max_leakrate and leak_rate_err < max_leakrate/10:
                                        print("FAILURE SHAME DISHONOR: Straw in chamber %.0f has failed, Please remove and reglue ends" % f)
                                        straw_status = "Failed leak requirement"
                                        #failed()
                                        #save to csv file
                                        if Choosenames[f][:7] in straw_list:
                                                break
                                        else:
                                                print("Enter anykey then go to saving data procedure:")
                                                endtime = time.time() + 1.5
                                                while True:
                                                        if msvcrt.kbhit():
                                                                c = input("save data for this straw?(y/n):")
                                                                straw_list.append(Choosenames[f][:7])
                                                                if c == 'y' or c == 'Y':
                                                                        result.write(Choosenames[f][:7] + ",")
                                                                        result.write(currenttime + ",")
                                                                        result.write("CO2"+",")
                                                                        result.write("wb0001"+",")
                                                                        result.write("ch" + str(f) + ",")
                                                                        result.write(str(leak_rate) + ",")
                                                                        result.write(str(leak_rate_err) + "\n")
                                                                break
                                                        if time.time() > endtime:
                                                                break
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
                                         'Slope = %.2f +- %.2f x $10^{-3}$ PPM/sec \n' % (slope[f]*10**4,slope_err[f]*10**4) +\
                                         'Leak Rate = %.2f +- %.2f x $10^{-5}$ cc/min \n' % (leak_rate *(10**5),leak_rate_err*(10**5)) +\
                                         straw_status+"\t"+currenttime,
                                         fontsize = 12, color = 'r')
                                plt.savefig('C:\\Users\\vold\\Desktop\\Leak Test Results\\'+ Choosenames[f] + '_fit.pdf')
                                plt.clf()

                #Check if we need to change straws
                if Need_for_change() :
                        for f in range(number_of_chambers):
                                files[f].close()
                        Update_names()


for f in range(number_of_chambers):
        files[f].close()



