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
        return 'first/'
    if (index == 2):
        return 'second/'
    if (index == 3):
        return 'third/'

    return 'NOPE/'

# based on XX:XX time, find index for array
def time_to_index(time, orig_day):
	t = time.split(" ")
	date = t[0]
	dm = date.split("/")
	day = int(dm[1])

	og_dm = orig_day.split("/")
	og_day = int(og_dm[1])
	if (day < og_day):
		day = day + 30
	day_diff = day - og_day
	print day_diff

	time = t[1]
	hm = time.split(":")
	hour = int(hm[0])
	mins = int(hm[1])

	index =  hour*60 + mins
	return index + 1440*day_diff

tracker = 1
while (tracker <= 3):
	dir_name = get_name(tracker)
	splice = dir_name.split('/')
	floor = splice[0]
	print floor
	# get all files for desired floor
	mypath = 'pre_data/'+dir_name

	orig_day = "10/25/16"

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
		fo_array = [0] * 10080  # array for each minute of the given sensor
		prev_active_time = -1

		# read in all entries 
		entry = fo.readline()
		while (entry != ""):
			print entry
			# record minute's status in global time-sequenced array
			values = entry.split("\t")
			cur_time = values[0]
			cur_status = int(values[1])
			index = time_to_index(cur_time, orig_day)

			# if sensor is active, mark in array
			if (cur_status == 1):
				fo_array[index] = 1
				prev_active_time = cur_time

			entry = fo.readline()

		# add sensor data to full data matrix
		global_array.append(list(fo_array))
		i = i + 1
	tup = []
	for i in range(len(global_array)):
		add = (names[i], global_array[i])
		tup.append(add)

	data_name = "experiment_data/" + floor + "_week.txt"
	file_out = open(data_name, 'w')
	for x in range(0,10080):
		for y in range(len(global_array)):
			cur_list = global_array[y]
			file_out.write(str(cur_list[x])+'\t')
		file_out.write('\n')

	file_out.close()

	tracker = tracker + 1











