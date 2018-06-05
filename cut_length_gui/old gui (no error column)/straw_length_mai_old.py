import sys
from PyQt4 import QtGui
#from straw_length import Ui_Dialog
import straw_length
import csv
import datetime
import os

# read in what lengths straws will be cut to
def getIntendedLength(filename):
    lengths = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) # skip header row
        for row in reader:
            length = row[1].strip()
            lengths.append(float(row[1]))
        open(filename).close()
    return lengths

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
    print(tempHumid)
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
        #   boxes of lengths to cut to
        intended_len = [self.intended_len_0, self.intended_len_1, self.intended_len_2, self.intended_len_3, self.intended_len_4, self.intended_len_5,
            self.intended_len_6, self.intended_len_7, self.intended_len_8, self.intended_len_9, self.intended_len_10,
            self.intended_len_11, self.intended_len_12, self.intended_len_13, self.intended_len_14, self.intended_len_15, self.intended_len_16,
            self.intended_len_17, self.intended_len_18, self.intended_len_19, self.intended_len_20, self.intended_len_21,
            self.intended_len_22, self.intended_len_23]
        
        # get lengths to cut to based on panel type 
        if str(self.panelType.currentText()) == '0, 4':
            lengths2display = getIntendedLength('/home/sam/Desktop/cut_length_gui/cut_lengths/LaserInfo0,4.csv')
        elif str(self.panelType.currentText()) == '2, 6':
            lengths2display = getIntendedLength('/home/sam/Desktop/cut_length_gui/cut_lengths/LaserInfo2,6.csv')
        
        
        # get lowest and highest straw numbers
        low_num = str(self.lowest_st.text())
        high_num = str(self.highest_st.text())
        low_num = int(low_num.strip('st'))
        high_num = int(high_num.strip('st'))
        
        # populate list of straw names
        for i in range (0, high_num-low_num+1):
            straw[i].setText('st' + str(low_num+i).zfill(5))
            intended_len[i].setText(str( "%.3f" % lengths2display[i] ))
            #"%.2f" % a
    
    def save_data(self):
        straw = [self.straw_0, self.straw_1, self.straw_2, self.straw_3, self.straw_4, self.straw_5,
            self.straw_6, self.straw_7, self.straw_8, self.straw_9, self.straw_10,
            self.straw_11, self.straw_12, self.straw_13, self.straw_14, self.straw_15, self.straw_16,
            self.straw_17, self.straw_18, self.straw_19, self.straw_20, self.straw_21,
            self.straw_22, self.straw_23]
            
        #   boxes of lengths to cut to
        intended_len = [self.intended_len_0, self.intended_len_1, self.intended_len_2, self.intended_len_3, self.intended_len_4, self.intended_len_5,
            self.intended_len_6, self.intended_len_7, self.intended_len_8, self.intended_len_9, self.intended_len_10,
            self.intended_len_11, self.intended_len_12, self.intended_len_13, self.intended_len_14, self.intended_len_15, self.intended_len_16,
            self.intended_len_17, self.intended_len_18, self.intended_len_19, self.intended_len_20, self.intended_len_21,
            self.intended_len_22, self.intended_len_23]
            
        mlen = [self.mlen_0, self.mlen_1, self.mlen_2, self.mlen_3, self.mlen_4, self.mlen_5,
            self.mlen_6, self.mlen_7, self.mlen_8, self.mlen_9, self.mlen_10,
            self.mlen_11, self.mlen_12, self.mlen_13, self.mlen_14, self.mlen_15, self.mlen_16,
            self.mlen_17, self.mlen_18, self.mlen_19, self.mlen_20, self.mlen_21,
            self.mlen_22, self.mlen_23]
            
        low_straw = str(self.straw_0.text())
        high_straw = str(self.straw_23.text())
        savefile = low_straw+ '-' + high_straw + '.csv'
        
        f = open(savefile,'w') # save info
        f.write('straw, intended length, measured length\n')
        for i in range (0,24):
            f.write( str(straw[i].text()) )
            f.write(','),
            f.write( str(intended_len[i].text()) )
            f.write(','),
            f.write( str(mlen[i].text()) )
            f.write('\n')
        f.close()
        
    
    def upload_data():
        a = 1
        
        
        
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    app.exec_()
    getTempHumid('/home/sam/Desktop/cut_length_gui/temphumid_data/')#/450_center_2018-04-26_000001.csv
    print(fileLength('/home/sam/Desktop/cut_length_gui/temphumid_data/464_2018-04-26_000001.csv'))

if __name__ == "__main__":
    main()
