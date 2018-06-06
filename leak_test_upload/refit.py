# Program made by Sam Penders to refit leak rate data from first two hours of leak test
# from a certain day. Add in additional file selection criteria if necessary. This
# writes the leak rates to a file for that day. This saves a csv
# data file in the same directory as the raw data.
# Made on 6-6-2018

from Run_Fit import fit
import os

def main():	
	date = '2018_06_05' # date to fit on
	directory = 'C:\\Users\\vold\\Desktop\\LeakTestGUI - Current Version\\Leak Test Results\\'
	items = os.listdir(directory) # data file names
	
	savefile = date + '_leakrates.csv' # file to write leak rates to
	f = open(directory + savefile,'w')
	f.write('straw,leakrate (*10^5 CC/hr),leakrate error (*10^5 CC/hr), chamber\n')
	
	for datafile in items:
		if datafile.endswith(date + '_rawdata.txt') and not datafile.startswith('.'):
			straw = datafile[0:7]
			leakrate, leakrate_error, ch = fit(directory + str(datafile))
			f.write(straw+',')
			f.write( str( round(float(leakrate)*10**5,2))+',' )
			f.write( str( round(float(leakrate_error)*10**5,2))+',' )
			f.write( str(ch) )
			f.write('\n')				
	f.close()	
	print('Done fitting. Find data file in ' + directory + savefile)
	input()
main()

