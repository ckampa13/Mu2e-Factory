#
#   program to run GUI for recording lengths that straws were cut to
#   Written by Sam Penders, Spring 2018 (pende061@umn.edu)
#   


import sys
from PyQt4 import QtGui
#from straw_length import Ui_Dialog
import straw_length
import csv
import datetime
import os
import time
from length_uploading import createLengthRow, uploadLengths

#---------------------------------------------------------------
# TO DO
# - check straw length correction relationships


# read in what lengths straws will be cut to
# return in 64th and inch part
def getIntendedLength(filename):
    C_T = 9.4e-6 # temp coefficient
    C_H = 9.6e-6 # humid coefficient
    tempHumid = getTempHumid('/home/sam/Desktop/cut_length_gui/temphumid_data')
    deltaT = tempHumid[0]*9.0/5.0 + 32 - 68 # relative to 68 F
    deltaH = tempHumid[1] # 0% - current humid %
    
    lengths_dec = [] # decimal length
    lengths_in = [] # inch part
    lengths_64 = [] # 1/64" part
    with open(filename) as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        next(datareader) # skip header row
        for row in datareader:
            length = float(row[1].strip())
            length = length/(1 + C_T*deltaT + C_H*deltaH) # correct for temp, humid
            
            lengths_dec.append(length)
            lengths_in.append( int(length) )
            
            _64th = (length % 1)*64
            lengths_64.append(_64th)
        
        open(filename).close()
    return lengths_dec, lengths_in, lengths_64

# this works as intended -- checked that it returns correct values
# return avg humidity and temp over last 30 min
def getTempHumid(directory):
    tempHumid = [0,0]
    currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
    
    allfiles = os.listdir(directory)
    for datafile in allfiles:
        if datafile.startswith('464_') and (currentDate in datafile):
            with open(directory + datafile,'r') as textfile:
                i = 1
                for row in reversed(list(csv.reader(textfile))): # read last 180 lines
                    if i <= 180:
                        tempHumid[0] = tempHumid[0] + float(row[1]) # sum up temperature
                        tempHumid[1] = tempHumid[1] + float(row[2]) # sum up humidity
                    if i > 180:
                        break
                    i = i + 1
            #with open(directory + datafile) as csvfile: 
                #reader = csv.reader(csvfile, delimiter=',')
                #i = 1
                #for row in reader:
                    #if i > fileLength(directory + datafile) - 180:
                        #tempHumid[0] = tempHumid[0] + float(row[1]) # sum up temperature
                        #tempHumid[1] = tempHumid[1] + float(row[2]) # sum up humidity
                    #i = i + 1
                #open(directory + datafile).close()
        
    tempHumid[0] = tempHumid[0]/180 # avg temp over last 30 min
    tempHumid[1] = tempHumid[1]/180 # avg humid over last 30 min
    return tempHumid
    

    
# checked--gives correct value
def fileLength(fullfilename): # get number of lines in file
    f = open(fullfilename,'r')
    i = 0
    for line in f:
        i = i + 1
    return i
    

class MyWindow(QtGui.QMainWindow, straw_length.Ui_MainWindow):
    def __init__(self):
        
        super(self.__class__, self).__init__()
        self.setupUi(self) 
 
        self.show()
        
    def straw_names(self):
        straw = [self.straw_0, self.straw_1, self.straw_2, self.straw_3, self.straw_4, self.straw_5,
            self.straw_6, self.straw_7, self.straw_8, self.straw_9, self.straw_10,
            self.straw_11, self.straw_12, self.straw_13, self.straw_14, self.straw_15, self.straw_16,
            self.straw_17, self.straw_18, self.straw_19, self.straw_20, self.straw_21,
            self.straw_22, self.straw_23]
        return straw
        
        
    def fill_info(self): # populate info when 'enter' button is hit
        
        # straw names
        straw = [self.straw_0, self.straw_1, self.straw_2, self.straw_3, self.straw_4, self.straw_5,
            self.straw_6, self.straw_7, self.straw_8, self.straw_9, self.straw_10,
            self.straw_11, self.straw_12, self.straw_13, self.straw_14, self.straw_15, self.straw_16,
            self.straw_17, self.straw_18, self.straw_19, self.straw_20, self.straw_21,
            self.straw_22, self.straw_23]
        
        # get lengths to cut to based on panel type 
        if str(self.panelType.currentText()) == '0, 4':
            intended_length = getIntendedLength('/home/sam/Desktop/cut_length_gui/cut_lengths/LaserInfo0,4.csv')
        elif str(self.panelType.currentText()) == '2, 6':
            intended_length = getIntendedLength('/home/sam/Desktop/cut_length_gui/cut_lengths/LaserInfo2,6.csv')
        
        # get lowest and highest straw numbers
        low_num = str(self.lowest_st.text())
        high_num = str(self.highest_st.text())
        low_num = int(low_num.strip('st'))
        high_num = int(high_num.strip('st'))
        
        # populate list of straw names
        for i in range (0, high_num-low_num+1):
            straw[i].setText('st' + str(low_num+i).zfill(5))
    
    def getError(self): # get difference between measured and intended length
        mlen = [self.mlen_0, self.mlen_1, self.mlen_2, self.mlen_3, self.mlen_4, self.mlen_5,
            self.mlen_6, self.mlen_7, self.mlen_8, self.mlen_9, self.mlen_10,
            self.mlen_11, self.mlen_12, self.mlen_13, self.mlen_14, self.mlen_15, self.mlen_16,
            self.mlen_17, self.mlen_18, self.mlen_19, self.mlen_20, self.mlen_21,
            self.mlen_22, self.mlen_23]
        
        # the 1/64" part of length measurement    
        mlen_64 = [self.mlen_64th_0, self.mlen_64th_1, self.mlen_64th_2, self.mlen_64th_3, self.mlen_64th_4, self.mlen_64th_5,
            self.mlen_64th_6, self.mlen_64th_7, self.mlen_64th_8, self.mlen_64th_9, self.mlen_64th_10,
            self.mlen_64th_11, self.mlen_64th_12, self.mlen_64th_13, self.mlen_64th_14, self.mlen_64th_15, self.mlen_64th_16,
            self.mlen_64th_17, self.mlen_64th_18, self.mlen_64th_19, self.mlen_64th_20, self.mlen_64th_21,
            self.mlen_64th_22, self.mlen_64th_23]
            
        error = [self.error_0, self.error_1, self.error_2, self.error_3, self.error_4, self.error_5,
            self.error_6, self.error_7, self.error_8, self.error_9, self.error_10,
            self.error_11, self.error_12, self.error_13, self.error_14, self.error_15, self.error_16,
            self.error_17, self.error_18, self.error_19, self.error_20, self.error_21,
            self.error_22, self.error_23]
            
        if str(self.panelType.currentText()) == '0, 4':
            intended_dec, intended_in, intended_64 = getIntendedLength('/home/sam/Desktop/cut_length_gui/cut_lengths/LaserInfo0,4.csv')
        elif str(self.panelType.currentText()) == '2, 6':
            intended_dec, intended_in, intended_64 = getIntendedLength('/home/sam/Desktop/cut_length_gui/cut_lengths/LaserInfo2,6.csv')
            
        for i in range (0,23):
            if( mlen[i].text() != '' and mlen_64[i].text() != '' ):
                difference = -1.0*((intended_in[i] - int(mlen[i].text()))*64 + (intended_64[i] - float(mlen_64[i].text())))
                difference = round(difference,1)
                error[i].setText(str(difference))
                
                # set box background to red if difference over 0.5/64"
                if(abs(difference) > 0.5):
                    error[i].setStyleSheet("background-color: rgb(255, 0, 0);")
                else:
                    error[i].setStyleSheet("background-color: rgb(255, 255, 255);")

            
        
    
    def save_data(self):
        straw = [self.straw_0, self.straw_1, self.straw_2, self.straw_3, self.straw_4, self.straw_5,
            self.straw_6, self.straw_7, self.straw_8, self.straw_9, self.straw_10,
            self.straw_11, self.straw_12, self.straw_13, self.straw_14, self.straw_15, self.straw_16,
            self.straw_17, self.straw_18, self.straw_19, self.straw_20, self.straw_21,
            self.straw_22, self.straw_23]
        
        # the inch part of length measurement   
        mlen = [self.mlen_0, self.mlen_1, self.mlen_2, self.mlen_3, self.mlen_4, self.mlen_5,
            self.mlen_6, self.mlen_7, self.mlen_8, self.mlen_9, self.mlen_10,
            self.mlen_11, self.mlen_12, self.mlen_13, self.mlen_14, self.mlen_15, self.mlen_16,
            self.mlen_17, self.mlen_18, self.mlen_19, self.mlen_20, self.mlen_21,
            self.mlen_22, self.mlen_23]
        
        # the 1/64" part of length measurement    
        mlen_64 = [self.mlen_64th_0, self.mlen_64th_1, self.mlen_64th_2, self.mlen_64th_3, self.mlen_64th_4, self.mlen_64th_5,
            self.mlen_64th_6, self.mlen_64th_7, self.mlen_64th_8, self.mlen_64th_9, self.mlen_64th_10,
            self.mlen_64th_11, self.mlen_64th_12, self.mlen_64th_13, self.mlen_64th_14, self.mlen_64th_15, self.mlen_64th_16,
            self.mlen_64th_17, self.mlen_64th_18, self.mlen_64th_19, self.mlen_64th_20, self.mlen_64th_21,
            self.mlen_64th_22, self.mlen_64th_23]
            
        error = [self.error_0, self.error_1, self.error_2, self.error_3, self.error_4, self.error_5,
            self.error_6, self.error_7, self.error_8, self.error_9, self.error_10,
            self.error_11, self.error_12, self.error_13, self.error_14, self.error_15, self.error_16,
            self.error_17, self.error_18, self.error_19, self.error_20, self.error_21,
            self.error_22, self.error_23]
        
        # intended straw lengths in decimal, inch part, and 1/64 part
        if str(self.panelType.currentText()) == '0, 4':
            intended_dec, intended_in, intend_64 = getIntendedLength('/home/sam/Desktop/cut_length_gui/cut_lengths/LaserInfo0,4.csv')
        elif str(self.panelType.currentText()) == '2, 6':
            intended_dec, intended_in, intend_64 = getIntendedLength('/home/sam/Desktop/cut_length_gui/cut_lengths/LaserInfo2,6.csv')
            
        worker1 = self.worker_barcode1.text()
        worker2 = self.worker_barcode2.text()

            
        low_straw = str(self.lowest_st.text())
        high_straw = str(self.highest_st.text())
        in_file_date = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        savedate = datetime.datetime.now().strftime('%Y-%m-%d')
        savefile = '/home/sam/Desktop/cut_length_gui/length_data/' + low_straw + '-' + high_straw + '_' + savedate + '.csv'
        
        # write data to file
        f = open(savefile,'w') # save info
        f.write('straw,intended length (in.),measured length (in), measured - intended (in) ,worker id1, worker id2, time (yyyy-mm-dd_HHMMSS)\n')
        for i in range (0,24):
                
                if( mlen[i].text() != '' and  mlen_64[i].text() != '' ):
                    measured_dec = float(mlen[i].text()) + float(mlen_64[i].text())/64
                    measured_dec = round(measured_dec,4)
                    difference = round(measured_dec - intended_dec[i],4)
                else:
                    difference = ''
                    measured_dec = ''
                
                f.write( str(straw[i].text()) )
                f.write(',')
                f.write(str(round(intended_dec[i],4))) 
                f.write(',')
                f.write( str(measured_dec) )
                f.write(',')
                #f.write( str(mlen[i].text()) )
                #f.write(',')
                #f.write( str(mlen_64[i].text()) )
                #f.write(',')
                f.write( str(difference) )
                f.write(',')          
                f.write(worker1)
                f.write(',')
                f.write(worker2)
                f.write(',')
                f.write(in_file_date)
                f.write('\n')
        f.close()
     
     # this should work as soon as we figure out database and adjust
     # data fields accordingly   
    def upload_data(self):
        self.save_data()
        
        low_straw = str(self.lowest_st.text())
        high_straw = str(self.highest_st.text())
        savedate = datetime.datetime.now().strftime('%Y-%m-%d')
        savefile = '/home/sam/Desktop/cut_length_gui/length_data/' + low_straw + '-' + high_straw + '_' + savedate + '.csv'
        
        with open(savefile) as csvfile:
            filereader = csv.reader(csvfile,delimiter = ',') 
            next(filereader)   
            for datarow in filereader:
                print(datarow)
                uploadLengths(datarow)
  
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    app.exec_()
    
if __name__ == "__main__":
    main()


























