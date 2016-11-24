# get count of times a sensor is the only sensor in the hall to be activated
# get count of times a sensor and at least one of its direct neighbors are the only ones to be activated

import sys
import os
from os import listdir
from os.path import isfile, join
import glob

# check if the items in active (indices between 0 and 5, representing column in data file)
# are neighbors based on the floor in question
# active list can be up to length 6 (all sensors) but in this implementation is only length 2 or 3
# def check_neighbors(active, floor):

# 	if (floor == "first"):

# 	if (floor == "second"):

# 	if (floor == "third"):

# read in files 
# should be of format given in Animate/animate_data/ direction (row per minute showing all activation)
# want to get locality data by floor - floor is user input 
print '\n'
day_input = raw_input("What days would you like to see? (enter space delimited)\n")
if (day_input == "all"):
	day_input = "monday tuesday weds thurs friday saturday sunday"
if (day_input == "weekend"):
	day_input = "saturday sunday"
if (day_input == "weekday"):
	day_input = "monday tuesday weds thurs friday"
floor = raw_input("What floor would you like to see? (choose 1: first, second, or third)\n")
floor_caps = floor.capitalize()
print '\n'
# get all files for given floor and time period
mypath = ""
files = []
if (day_input == "all"):
	mypath = 'Animate/animate_data/global_'+'*'+floor+'.txt'
	files = glob.glob(mypath)
else:
	days = day_input.split(" ")
	for day in days:
		path = 'Animate/animate_data/global_'+day+'_'+floor+'.txt'
		files.append(path)

# generate data on the locality of activity
single_active_freq = 0   # a single sensor and no other sensors activated
neighbors_active = 0     # only a cluster of neighbors activated (up to size 3)
all_active = 0           # every sensor activated

correlations = []
on_frequencies = []
# find number of times others are active when sensor X is active
for sensor in range(6):
	corr_count = 0
	active_corr_count = [0] * 6 
	on_freq = 0 
	for f in files:
		fo = open(f, "rw+")
		entry = fo.readline()

		while (entry != ""):
			data = entry.split('\t')
			# scan through 6 places and find active points
			# add to list of active sensors
			if (data[sensor] != "1"):
				entry = fo.readline()
				continue
			else:
				on_freq = on_freq+1
				# check each entry and incrememnt mutual acitvation count if active
				for index in range(len(data)):
					if (data[index] == "1"):
						corr_count = corr_count + 1
						active_corr_count[index] = active_corr_count[index] + 1
			entry = fo.readline()

		fo.close()
	on_frequencies.append(on_freq)
	correlations.append(active_corr_count)

i = 0
print "frequency of activation by sensor: "  
print on_frequencies 
print '\n'
for cor in correlations:
	print "correlations " + str(i) + ": " + str(cor)
	i = i + 1
print '\n'
# for f in files:

# 	fo = open(f, "rw+")
# 	entry = fo.readline()

# 	while (entry != ""):
# 		data = entry.split('\t')
# 		# scan through 6 places and find active points
# 		# add to list of active sensors
# 		active = []
# 		index = 0
# 		for d in data:
# 			if (d == "1"):
# 				active.append(index)
# 			index = index + 1
# 		# if no more than three sensors
# 		if (len(active) == 1):
# 			single_active_freq = single_active_freq + 1
# 		elif (len(active) == 2 || len(active) == 3):
# 			neighbors = check_neighbors(active,floor)
# 			if (neighbors):
# 				neighbors_active = neighbors_active + 1
# 		elif (len(active) == 6):
# 			all_active = all_active + 1

# 		entry = fo.readline

# 	fo.close()
# print "single active: "+ single_active_freq 
# print "neighborhood cluster active: " + neighbors_active
# print "all sensors active: "+ all_active


