import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import os
import csv
from scipy.stats import norm

data_file = 'channel_01oo_raw_data.csv'

#data_file2 = 'channel_02oo_raw_data.csv'

data_directory = 'sorted_channel_data\\'

new_file = '_histo_plain.pdf'
new_directory = 'channel_histos\\'

good_range_oo = [80,140]

meas_type_flag = 'oo'
calc_type_flag = 'B'

new_file = '_' + calc_type_flag + new_file
new_directory += meas_type_flag + '\\' + calc_type_flag + '\\'

def loadData(dat_dir,dat_fil,calc_flag):
    loaded_data = []
    with open(dat_dir+dat_fil, newline='') as csvfile:
        csvRead = csv.reader(csvfile, delimiter=',', quotechar='|')
        i = 0
        for row in csvRead:
            if (i != 0):
                if (row[1].replace(' ','') == calc_flag):
                    data_point = float(row[0])
                    loaded_data.append(data_point)
            i += 1
    return dat_fil[8:12], loaded_data

def calculate_in_range(dat,good_range):
    #np_dat = np.array(data_list)
    num_in_range = 0
    num_non_con = 0
    for i in dat:
        if i == 99999:
            num_non_con += 1
        if i >= good_range[0] and i <= good_range[1]:
            num_in_range +=1
    return num_in_range/len(dat), num_non_con/len(dat)

def fitStats(histo_data):
    (mu, sigma) = norm.fit(histo_data)
    return mu, sigma
    

def histoPlot(chan_name,calc_type,data_list,mu,sig):
    fig, ax = plt.subplots()
    
    binwidth = 5
    binslist = range(80,310,binwidth)
    
    #ax.hist(np.clip(data_list, binslist[0], binslist[-1]), bins = binslist, facecolor='blue', edgecolor='black', linewidth=1)
    ax.hist(np.clip(data_list, binslist[0], binslist[-1]), bins = binslist, normed=1, facecolor='blue', edgecolor='black', linewidth=1)
    
    #plot fit
    y = mlab.normpdf(binslist,mu,sig)
    ax.plot(binslist,y,'r--',linewidth=1.5)
    
    
    ax.set_xlabel(r'Resistance ($\Omega$)')
    ax.set_ylabel(r'Frequency')
    ax.set_title(r'$\mathrm{Channel\ %s\ Method\ %s:}\ \mu=%.3f,\ \sigma=%.3f$' %(chan_name,calc_type,mu, sig))
    
    ax.set_axisbelow(True)
    ax.xaxis.grid(color='gray', linestyle='dashed')
    ax.yaxis.grid(color='gray', linestyle='dashed')
    
    plt.grid(True)
    plt.show()
    
def histoPlotSave(chan_name,calc_type,data_list,new_dir,new_fil):
    fig, ax = plt.subplots()
    
    binwidth = 5
    binslist = range(80,310,binwidth)
    
    ax.hist(np.clip(data_list, binslist[0], binslist[-1]), bins = binslist, facecolor='blue', edgecolor='black', linewidth=1)

    ax.set_xlabel(r'Resistance ($\Omega$)')
    ax.set_ylabel(r'Frequency')
    ax.set_title(r'$\mathrm{Channel\ %s\ Method\ %s}$' % (chan_name,calc_type))
    
    ax.set_axisbelow(True)
    ax.xaxis.grid(color='gray', linestyle='dashed')
    ax.yaxis.grid(color='gray', linestyle='dashed')
    
    plt.grid(True)
    plt.savefig(new_dir + chan_name + new_fil)
    plt.close()

def main():
    files = [f for f in os.listdir(data_directory) if f[10:12]==meas_type_flag]
    #files = data_file
    for ch in files:
        channel_name, channel_data = loadData(data_directory,ch,calc_type_flag)
        in_range, non_con = calculate_in_range(channel_data,good_range_oo)
        print('Channel %s %s: %% non-conduct = %f, %% in-range = %f' % (channel_name, calc_type_flag, non_con, in_range)) 
        mu, sigma = fitStats(channel_data)
        histoPlot(channel_name,calc_type_flag,channel_data,mu,sigma)
        #histoPlotSave(channel_name, calc_type_flag, channel_data, new_directory, new_file)
    input('Press enter to exit...')

main()
