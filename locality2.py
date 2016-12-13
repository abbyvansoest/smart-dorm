# get count of times a sensor is the only sensor in the hall to be activated
# get count of times a sensor and at least one of its direct neighbors are the only ones to be activated

import sys
import os
from os import listdir
from os.path import isfile, join
import glob

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
		f_out = open("local_activation/locality"+str(sensor)+".txt", "w")

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
				tot_active = tot_active + 1
				on_freq = on_freq+1
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

		fo.close()



