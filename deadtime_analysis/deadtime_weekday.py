#  weekdays in one color
#  weekends in another
#  NORMALIZE counts

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from os import listdir
from os.path import isfile, join

def calculate_time_diff(prev_time, cur_time):

	diff = -1
	
	# split at space character into (date) and (time)
	t1 = prev_time.split(" ")
	date1 = t1[0]
	time1 = t1[1]
	hm1 = time1.split(":")
	hour1 = int(hm1[0])
	min1 = int(hm1[1])

	t2 = cur_time.split(" ")
	date2 = t2[0]
	time2 = t2[1]
	hm2 = time2.split(":")
	hour2 = int(hm2[0])
	min2 = int(hm2[1])

	h_diff = hour2 - hour1
	if (h_diff < 0):
		h_diff = 24 + h_diff
	m_diff = min2 - min1
	if (h_diff == 0):
		diff = m_diff
	elif (m_diff < 0):
		diff = (60 + m_diff)
	else:
		diff = (h_diff*60 + m_diff)
	return diff


fig = plt.figure()
threshold = 200
count = [0 for i in range(threshold+1)]
weekday_path = 'data/by_weekday/weekday/'
weekend_path = 'data/by_weekday/weekend/'
dest_dir = 'histograms/by_weekday/'
weekday = [f for f in listdir(weekday_path) if isfile(join(weekday_path, f))]
weekend = [f for f in listdir(weekend_path) if isfile(join(weekend_path, f))]

if '.DS_Store' in weekday: weekday.remove('.DS_Store')
if '.DS_Store' in weekend: weekend.remove('.DS_Store')

# Open each weekday file and run to develop a histogram
mins_between_wkdy = []
for f_wkdy in weekday:
	name, extension = os.path.splitext(f_wkdy)
	fo = open(weekday_path+f_wkdy, "rw+")

	prev_entry = fo.readline() # first active time to init things
	first_vals = prev_entry.split("\t")
	prev_time = first_vals[0]

	# read in all data and record time differences between activation
	entry = fo.readline()
	max_diff = -1

	while (entry != ""):
		values = entry.split("\t")
		cur_time = values[0]
		cur_status = int(values[1])

		if (cur_time == prev_time):
			entry = fo.readline()
			continue

		if (cur_status == 1):
			time_diff = calculate_time_diff(prev_time, cur_time)
			if (time_diff > max_diff):
				max_diff = time_diff
			if (time_diff <= threshold):
				mins_between_wkdy.append(time_diff)
				count[time_diff] = count[time_diff] + 1
			prev_time = cur_time

		entry = fo.readline()
	
# create historgram for all weekdays
mins_between_wknd = []
for f_wknd in weekend:
	name, extension = os.path.splitext(f_wknd)
	fo = open(weekend_path+f_wknd, "rw+")

	prev_entry = fo.readline() # first active time to init things
	first_vals = prev_entry.split("\t")
	prev_time = first_vals[0]

	# read in all data and record time differences between activation
	entry = fo.readline()
	max_diff = -1

	while (entry != ""):
		values = entry.split("\t")
		cur_time = values[0]
		cur_status = int(values[1])

		if (cur_time == prev_time):
			entry = fo.readline()
			continue

		if (cur_status == 1):
			time_diff = calculate_time_diff(prev_time, cur_time)
			if (time_diff > max_diff):
				max_diff = time_diff
			if (time_diff <= threshold):
				mins_between_wknd.append(time_diff)
				count[time_diff] = count[time_diff] + 1
			prev_time = cur_time

		entry = fo.readline()

mins_between_wkdy_norm = mins_between_wkdy/np.linalg.norm(mins_between_wkdy)
mins_between_wknd_norm = mins_between_wknd/np.linalg.norm(mins_between_wknd)

# min1 = min(mins_between_wkdy_norm)
# min2 = min(mins_between_wknd_norm)
# max1 = max(mins_between_wkdy_norm)
# max2 = max(mins_between_wknd_norm)

# plt_range = range(min(min1, min2), 60)
# bins = max(plt_range) # number of bins to use 

n, bins, patches = plt.hist([mins_between_wkdy_norm, mins_between_wknd_norm], 100, range=[0,.15], histtype='bar', color=['crimson', 'burlywood'])
plt.legend('upper right')

save_name = dest_dir + 'figure' +'.png'
plt.savefig(save_name)
plt.show() 


