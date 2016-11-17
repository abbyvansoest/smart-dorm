# takes in data from a single occupancy sensor in Bloomberg Hall
# calculated the time between "on" events for that sensor
# displays a historgram of the frequency of those "dead" periods

# data needs to be a simple text file with each entry taking up two line
	# first line is date/time string
	# second line is on or off in terms of 0/1

import pylab as plt
import sys
import os
from os import listdir
from os.path import isfile, join
from operator import add

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
threshold = 150
count = [0 for i in range(threshold+1)]
mypath = 'data/before_school/'
dest_dir = 'histograms/before_school/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

if '.DS_Store' in files: files.remove('.DS_Store')

cumulative = [0] * threshold

# Open each file and run to develop a histogram
for f in files:
	name, extension = os.path.splitext(f)
	fo = open(mypath+f, "rw+")

	mins_between = [] # vector for all time diffs

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
				mins_between.append(time_diff)
				count[time_diff] = count[time_diff] + 1
			prev_time = cur_time

		entry = fo.readline()

	n, bins, patches = plt.hist(mins_between, bins=range(0, threshold+1,1), normed=True)
	save_name = dest_dir + name + '_2' + '.png'
	plt.title(name + ' Sensor, Dead Time Frequency')
	plt.xlabel('Time Since Last Activation')
	plt.ylabel('Frequency')
	plt.savefig(save_name)
	#plt.show()

	cumulative = map(add, cumulative, n)
	print cumulative


n, bins, patches = plt.hist(cumulative, bins=range(0, threshold+1,1), normed=True)
plt.title('Dead Time Frequency Over All Sensors: Before School') 
plt.xlabel('Time Since Last Activation')
plt.ylabel('Frequency')
save_name = 'global_before_school' +'.png'
plt.savefig(save_name)
plt.show() 



