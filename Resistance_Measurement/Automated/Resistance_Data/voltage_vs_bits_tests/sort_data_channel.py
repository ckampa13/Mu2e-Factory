# sort all of the data files by each channel (i.e. straw 10, i-i)
# note: should sort
# note: include calculation method as well: ref voltage vs bits only
# csv: [0], straw id; [4], resistance measurement


import numpy as np
import os
import csv

##***Global Variables***##
data_flag = 'resistance'
data_directory = 'raw_data'
save_directory = 'sorted_channel_data'
new_name = 'channel_'

straw_nums = {'st00001':'24','st00002':'23','st00003':'22','st00004':'21',
              'st00005':'20','st00006':'19','st00007':'18','st00008':'17',
              'st00009':'16','st00010':'15','st00011':'14','st00012':'13',
              'st00013':'12','st00014':'11','st00015':'10','st00016':'09',
              'st00017':'08','st00018':'07','st00019':'06','st00020':'05',
              'st00021':'04','st00022':'03','st00023':'02','st00024':'01'}

##***Functions***##
def loadData(flag,data_dir,straws):
    print('Loading and sorting data...')
    files = [f for f in os.listdir(data_dir) if f.startswith(flag)]
    separated_data = {}
    j = 0
    for data_run in files:
        letter = data_run[10]
        with open(data_dir + '\\' + data_run, newline='') as csvfile:
            csvRead = csv.reader(csvfile, delimiter=',', quotechar='|')
            i = 0
            for row in csvRead:
                if (i != 0):
                    key = straws[row[0].replace(' ','')]
                    meas_type = row[7].replace(' ', '')
                    if meas_type == 'inside-inside':
                        key += 'ii'
                    elif meas_type == 'inside-outside':
                        key += 'io'
                    elif meas_type == 'outside-inside':
                        key += 'oi'
                    elif meas_type == 'outside-outside':
                        key += 'oo'
                    else:
                        key += 'err'
                    dummy = row[4].replace(' ','')
                    if dummy == 'inf':
                        dummy = '99999'
                    if j == 0:
                        separated_data[key] = [[dummy,letter]]
                    else:
                        separated_data[key].append([dummy,letter])
                i += 1
        j += 1
    return separated_data

def saveFile(data_dic, new_filename, new_dir):
    print('Saving sorted data...')
    for key, data_lists in data_dic.items():
        with open(new_dir + '\\' + new_filename + key + '_raw_data.csv', 'w') as f:
            f.write('Resistance,Calculation Method\n')
            for data_points in data_lists:
                f.write(data_points[0] + ',' + data_points[1] + '\n')

def main():
    data_dict = loadData(data_flag, data_directory, straw_nums)
    saveFile(data_dict, new_name, save_directory)
    input('Press enter to exit...')

main()
