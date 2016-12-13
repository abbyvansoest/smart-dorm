# get count of times a sensor is the only sensor in the hall to be activated
# get count of times a sensor and at least one of its direct neighbors are the only ones to be activated

import sys
import os
from os import listdir
from os.path import isfile, join
import glob

# first
# ['OS_bloom_hall131', 'OS_bloom_hall132', 'OS_corr122', 'OS_Corr130A', 'OS_Corr132', 'OS_Hall121']
# 3 - 6, 4
# 6 - 3
# 2 - 5
# 5 - 2, 1
# 1 - 4, 5
# 4 - 1, 3

# second
# ['OS_Corr257', 'OS_Corr260', 'OS_Corr264', 'OS_Corr266', 'OS_Corr272', 'OS_Rm253']
# 6-1
# 1 - 6, 2, 3
# 2 - 1
# 3 - 1, 4
# 4 - 3, 5
# 5 - 4

# third
# ['OS_Corr356', 'OS_Corr357', 'OS_Corr360', 'OS_Corr364', 'OS_Corr366', 'OS_Rm353']
 
# 6 - 2
# 2 - 4, 3
# 1 - 3
# 3 - 1, 2
# 4 - 5, 2
# 5 - 4

def neighbors(index1, index2, floor):
	neighbors = False
	if (floor == "first"):
		if (index1 == 0):
			if (index2 == 3 or index2 == 4):
				neighbors = True
		if (index1 == 1):
			if (index2 == 4):
				neighbors = True
		if (index1 == 2):
			if (index2 == 3 or index2 == 5):
				neighbors = True	
		if (index1 == 3):
			if (index2 == 0 or index2 == 2):
				neighbors = True	
		if (index1 == 4):
			if (index2 == 0 or index2 == 1):
				neighbors = True
		if (index1 == 5):
			if (index2 == 2):
				neighbors = True

	if (floor == "second"):
		if (index1 == 0):
			if (index2 == 1 or index2 == 2 or index2 == 5):
				neighbors = True
		if (index1 == 1):
			if (index2 == 0):
				neighbors = True
		if (index1 == 2):
			if (index2 == 3 or index2 == 0):
				neighbors = True	
		if (index1 == 3):
			if (index2 == 2 or index2 == 4):
				neighbors = True	
		if (index1 == 4):
			if (index2 == 3):
				neighbors = True
		if (index1 == 5):
			if (index2 == 0):
				neighbors = True

	if (floor == "third"):
		if (index1 == 0):
			if (index2 == 2):
				neighbors = True
		if (index1 == 1):
			if (index2 == 2 or index2 == 3):
				neighbors = True
		if (index1 == 2):
			if (index2 == 0 or index2 == 1):
				neighbors = True	
		if (index1 == 3):
			if (index2 == 1 or index2 == 4):
				neighbors = True	
		if (index1 == 4):
			if (index2 == 3):
				neighbors = True
		if (index1 == 5):
			if (index2 == 1):
				neighbors = True
	return neighbors


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
print files
global_on_freq = 0

f_out = open("local_activation/locality_"+floor+".txt", "w")

# find number of times others are active when sensor X is active
for sensor in range(6):

	only_active = 0
	neighbors_active = 0   # number of times sensor in question is activated at the same time as one/both of neighbors 
	all_active = 0
	on_freq = 0 

	# go through each file
	for f in files:
		fo = open(f, "rw+")
		entry = fo.readline()

		# if that sensor is inactive, skip entry
		# otherwise, see if neighbors are active
		while (entry != ""):
			data = entry.split('\t')
			tot_active = 0
			# scan through 6 places and find active points
			# add to list of active sensors
			if (data[sensor] != "1"):
				entry = fo.readline()
				continue
		
			else:
				global_on_freq = global_on_freq + 1
				tot_active = tot_active + 1
				on_freq = on_freq + 1
				# check each entry and incrememnt mutual activation count if active
				for index in range(len(data)):
					if (index == sensor):
						continue
					if (data[index] == "1"):
						tot_active = tot_active + 1
						# if neighbors are active, increment
						if (neighbors(sensor, index, floor)):
							neighbors_active = neighbors_active + 1

				if (tot_active == 6):
					all_active = all_active + 1
				if (tot_active == 1):
					only_active = only_active + 1

			entry = fo.readline()

	f_out.write("total activity of sensor " + str(sensor)+": " + str(on_freq) + "\n")
	f_out.write("active at same time as 1+ neighbors: " + str(neighbors_active) + "\n")
	f_out.write("only sensor active: " + str(only_active) + "\n")
	f_out.write("*****************************************" + "\n")
	f_out.write("\n")
	fo.close()

f_out.write("total activity across all sensors: " + str(global_on_freq) + "\n")
f_out.close()



