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

def sum_line(line):
	sensor = line.split("\t")
	add = 0
	for i in range(len(sensor)):
		if (sensor[i] == "1"):
			add = add + 1
	return add


mypath = "Animate/animate_data/"
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
direct = "freq_by_hour/"
out_filename = direct+"full.txt"
out_txt = open(out_filename, "w")
if '.DS_Store' in files: files.remove('.DS_Store')


for f in files:

	hours = 24
	minutes = 60

	fo = open(mypath+f, "rw+")
	name, extension = os.path.splitext(f)
	splice = name.split("_")
	day = splice[1]
	floor = splice[2]

	out_txt.write(day + "\t" + floor+"\n")
	fd = day +"_"+floor+".txt"
	day_txt = open(direct+fd, "w")

	for hour in range(hours):

		hour_sum = 0

		# read in line of sensor data from that minute, 
		# convert to integers and sum 
		# add to overall sum for the hour
		if (hour == 23):
			minutes = 59
		for j in range(minutes): 
			line = fo.readline()
			hour_sum = hour_sum + sum_line(line)

		out_txt.write(str(hour_sum)+"\n")
		day_txt.write(str(hour_sum)+"\n")
	
	day_txt.close()

out_txt.close()		









