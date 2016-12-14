# takes in data from a udirectory of occupancy sensors in Bloomberg Hall
# calculated the time between "on" events for that sensor
# displays a historgram of the frequency of those deadtime periods
	# for individual sensros
	# for the accumulated average of those sensors

# data needs to be a simple text file with each entry taking up two line
	# first line is date/time string
	# second line is on or off in terms of 0/1

import pylab as plt
import sys
import os
from os import listdir
from os.path import isfile, join
from operator import add
from pandas import DataFrame
import openpyxl
import glob

# calculate the time difference between two sequential active events 
# prev time should come before cur_time - returns -1 otherwise
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

# based on array of minutes between events and the functional 
# threshold, find counts of minutes between events for each bucket
def get_counts(mins_between, threshold):

	# iterate through entire array
	# increment proper bin
	counts = [0] * threshold
	for diff in mins_between:
		if (diff > threshold-1):
			continue
		counts[diff] = counts[diff] + 1

	return counts

threshold = 151   # max value to record in frequency counts
xmax = 160        # max x-value in histogram
ymax = 1          # optional y-value to set 
count = [0 for i in range(threshold)]

# get all files for given time period
week = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
for day in week:
	day_caps = day.capitalize()
	mypath = 'Animate/pre_data/'+day
	path1 = mypath+'/first/*.txt'
	path2 = mypath+'/second/*.txt'
	path3 = mypath+'/third/*.txt'
	files1 = glob.glob(path1)
	files2 = glob.glob(path2)
	files3 = glob.glob(path3)

	dest_dir = 'breakdown/deadtime/'+day+'/'
	files = files1+files2+files3
# statistics trackers
cumulative = [0] * threshold
num_tot_events = 0
above_25 = 0
high_delays = 0
max_diff_arr = []

# Open each file and run to develop a histogram
for f in files:
	fig = plt.figure()
	name, extension = os.path.splitext(f)
	splited = name.split('/')
	this_name = splited[4]
	fo = open(f, "rw+")

	mins_between = [] # vector for all time diffs
	num_on_events = 0

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

		# if sensor is active, increment statistics and add to mins_between array
		# compare to threshold value to eliminate large outliers
		if (cur_status == 1):
			num_on_events = num_on_events + 1
			num_tot_events = num_tot_events + 1

			time_diff = calculate_time_diff(prev_time, cur_time)
			if (time_diff > max_diff):
				max_diff = time_diff
			if (time_diff < threshold):
				mins_between.append(time_diff)
				count[time_diff] = count[time_diff] + 1
			if (time_diff >= threshold):
				high_delays = high_delays + 1
			if (time_diff >= 25):
				above_25 = above_25 + 1
			prev_time = cur_time

		entry = fo.readline()

	num = []
	#max_diff_arr.append(max_diff)
	num = get_counts(mins_between, threshold)

	# plot and save individual sensor histogram for time period
	if (num_on_events == 0):
		this = 0
		# fdata = open(dest_dir+day+"_"+this_name+"_data"+'.txt', 'w')
		# fdata.write(str(num_on_events)+'\n')
		# fdata.close()
	else:
		n, bins, patches = plt.hist(mins_between, bins=range(0, threshold,1), normed=True)
		# save_name = dest_dir + day + "_" + this_name + '.png'
		# plt.title(this_name + ' Sensor, Dead Time Frequency ('+day_caps+')')
		# plt.xlabel('Time Since Last Activation')
		# plt.ylabel('Frequency')
		# plt.xlim(0., xmax)
		# plt.savefig(save_name)
		# fdata = open(dest_dir+day+"_"+this_name+"_data"+'.txt', 'w')
		# fdata.write(str(num_on_events)+'\n')
		# for x in n:
		# 	fdata.write(str(x)+'\n')
		# fdata.close()	

	# track cumulative counts over all sensors
	cumulative = map(add, cumulative, num)
	fo.close()

cum2 = [x+1 for x in cumulative]
#max_all = max(max_diff_arr)
# print max_diff_arr
# print "max dead " + repr(max_all)
# print "total on " + repr(num_on_events)
# print "total " + repr(num_tot_events)
# print "above thresh " + repr(high_delays) + " thresh is " + repr(threshold)
# print "above 25 " + repr(above_25)

# save dead time, cumulative, and cumulative nonzero counts for all daedtime values within range
index = range(0,threshold)
# df = DataFrame({'Dead Time': index, 'Total': cumulative, 'non-zero': cum2})
# df.to_excel('cumulative_before_school.xlsx', sheet_name='sheet1', index=False)

# plot cumulative histogram over all sensors
fig = plt.figure()
n, bins, patches = plt.hist(cumulative, bins=range(0, threshold,1), normed=True)
fdata = open(dest_dir+day+'_all_data.txt', 'w')
fdata.write(str(num_tot_events)+'\n')
for x in n:
	fdata.write(str(x)+'\n')
fdata.close()	

plt.title('Dead Time Frequency Over All Sensors: '+day_caps) 
plt.xlabel('Time Since Last Activation')
plt.ylabel('Frequency')
plt.xlim(0., xmax)
save_name = dest_dir+ day +'_all.png'
plt.savefig(save_name)
#plt.show() 



