# takes in data from a single occupancy sensor in Bloomberg Hall
# calculated the time between "on" events for that sensor
# displays a historgram of the frequency of those "dead" periods

# data needs to be a simple text file with each entry taking up two line
	# first line is date/time string
	# second line is on or off in terms of 0/1

import pylab as plt
import plotly.plotly as py
import sys

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
	if diff > 500:
		print time1
		print time2
		print diff
		print h_diff
		print m_diff
	return diff


fig = plt.figure()

# Open the file entered as a commandline argument
fo = open(sys.argv[1], "rw+")

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

	if (cur_status == 1):
		time_diff = calculate_time_diff(prev_time, cur_time)
		if (time_diff > max_diff):
			max_diff = time_diff
		mins_between.append(time_diff)
		prev_time = cur_time

	entry = fo.readline()
	
print mins_between
n, bins, patches = plt.hist(mins_between)
plt.show() 



