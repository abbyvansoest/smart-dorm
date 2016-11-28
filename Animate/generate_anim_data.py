# from set of sensor data over course of full day,
# generate a fully serialized minute-by-minute representation

# access data files for day
# keep organized by floor (i.e. save results by floor)

#--------------------------------#
# FIRST FLOOR
	# OS_bloom-hall131
	# OS_bloom-hall132
	# OS_corr122
	# OS_Corr130A
	# OS_Corr132
	# OS_Hall121

#SECOND FLOOR
	# OS_Corr257
	# OS_Corr260
	# OS_Corr264
	# OS_Corr266
	# OS_Corr272
	# OS_Rm253

# THIRD FLOOR
	# OS_Corr356
	# OS_Corr357
	# OS_Corr360
	# OS_Corr364
	# OS_Corr366
	# OS_Rm353

# so let's say i get all the daya for single days over the course of a full week
# what i need to do is develop a really big data matrix for each floor
	# for each sensor, activation status at each minute

import sys
import os
from os import listdir
from os.path import isfile, join
from operator import add
from pandas import DataFrame
import openpyxl

def get_name(index):

    if (index == 1):
        return 'tuesday/first/'
    if (index == 2):
        return 'tuesday/second/'
    if (index == 3):
        return 'tuesday/third/'
    if (index == 4):
        return 'weds/first/'
    if (index == 5):
        return 'weds/second/'
    if (index == 6):
        return 'weds/third/'
    if (index == 7):
        return 'thurs/first/'
    if (index == 8):
        return 'thurs/second/'
    if (index == 9):
        return 'thurs/third/'
    if (index == 10):
        return 'friday/first/'
    if (index == 11):
        return 'friday/second/'
    if (index == 12):
        return 'friday/third/'
    if (index == 13):
        return 'saturday/first/'
    if (index == 14):
        return 'saturday/second/'
    if (index == 15):
        return 'saturday/third/'
    if (index == 16):
        return 'sunday/first/'
    if (index == 17):
        return 'sunday/second/'
    if (index == 18):
        return 'sunday/third/'
    if (index == 19):
    	return 'monday/first/'
    if (index == 20):
    	return 'monday/second/'
    if (index == 21):
    	return 'monday/third/'

    return 'NOPE/'

# based on XX:XX time, find index for array
def time_to_index(time):
	t = time.split(" ")
	date = t[0]
	time = t[1]
	hm = time.split(":")
	hour = int(hm[0])
	mins = int(hm[1])

	index =  hour*60 + mins
	return index

tracker = 1
while (tracker <= 21):
	dir_name = get_name(tracker)
	splice = dir_name.split('/')
	day = splice[0]
	floor = splice[1]
	# get all files for desired day and floor
	mypath = 'pre_data/'+dir_name

	files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	if '.DS_Store' in files: files.remove('.DS_Store')
	global_array = []
	names = []
	i = 0

	# for each sensor in the hall
	for f in files:
		sensor_name, extension = os.path.splitext(f)
		names.append(sensor_name)
		fo = open(mypath+f, "rw+")
		fo_array = [0] * 1439  # array for each minute of the given sensor
		prev_active_time = -1

		# read in all entries 
		entry = fo.readline()
		while (entry != ""):

			# record minute's status in global time-sequenced array
			values = entry.split("\t")
			cur_time = values[0]
			cur_status = int(values[1])
			index = time_to_index(cur_time)

			# if sensor is active, mark in array
			if (cur_status == 1):
				fo_array[index] = 1
				prev_active_time = cur_time

			entry = fo.readline()

		# add sensor data to full data matrix
		global_array.append(list(fo_array))
		i = i + 1

	# tup = []
	# for i in range(len(global_array)):
	# 	add = (names[i], global_array[i])
	# 	tup.append(add)

	# my_dict = dict(tup)
	# df = DataFrame(my_dict)
	data_name = 'global_' +day+'_'+floor+'.txt'
	# df.to_excel(data_name, sheet_name='sheet1', index=False)
	file_out = open(data_name, 'w')
	for x in range(0,1439):
		for y in range(len(global_array)):
			cur_list = global_array[y]
			file_out.write(str(cur_list[x])+'\t')
		file_out.write('\n')

	file_out.close()

	tracker = tracker + 1












