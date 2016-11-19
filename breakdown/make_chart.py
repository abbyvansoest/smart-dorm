# build a frequency chart based off the data in frequency by hour // by day file

import numpy as np
import matplotlib.pyplot as plt

def check_input(days, floor):
	error = False
	if (floor != "first" and floor != "second" and floor != "third"):
		print "Not a valid floor!"
		error = True

	for day in days:
		if (day != "monday" and day != "tuesday" and day != "weds" and day != "thurs" and day != "friday" and day != "saturday" and day != "sunday"):
			if (day == "wednesday"):
				print "You used '" + day + "'. Use 'weds' instead!"
			elif (day == "thursday"):
				print "You used '" + day + "'. Use 'thurs' instead!"
			else:
				print day + " is not a day!"
			error = True

	if (error):
		quit()
	return

mydir = "freq_by_hour/"

day_input = raw_input("What days would you like to see? (enter space delimited)\n")
if (day_input == "all"):
	day_input = "monday tuesday weds thurs friday saturday sunday"
if (day_input == "weekend"):
	day_input = "saturday sunday"
if (day_input == "weekday"):
	day_input = "monday tuesday weds thurs friday"
floor = raw_input("What floor would you like to see? (choose 1: first, second, or third)\n")

days = day_input.split(" ")
check_input(days, floor)

# potential lists to graph
lists = []

N = 24
incr = 2.
ind = np.arange(0, incr*N, incr)
margin = .15
width = incr*(1.0 - 2.*margin)/len(days)

fig, ax = plt.subplots()

# for each desired day/floor, open the file for that combo
# and create a list of the 24 entries
# add to global list
for day in days:
	if day == "":
		continue
	day_list = []

	fname = day+"_"+floor+".txt"
	fo = open(mydir+fname, "rw+")

	for line in fo:
		day_list.append(int(line))
	lists.append(day_list)

# Add each day's frequency data to the chart
offset = 0
index = 0
legend_rects = []
for l in lists:

	#print data
	print '\n'+days[index] 
	for x in l:
		print str(x)

	if (days[index] == 'monday'):
		col = 'm'
	if (days[index] == 'tuesday'):
		col = 'b'
	if (days[index] == 'weds'):
		col = 'y'
	if (days[index] == 'thurs'):
		col = 'g'
	if (days[index] == 'friday'):
		col = 'c'
	if (days[index] == 'saturday'):
		col = 'r'
	if (days[index] == 'sunday'):
		col = 'k'
	rects = ax.bar(ind+margin+offset, l, width, color=col)
	legend_rects.append(rects[0])
	offset = offset + width
	index = index + 1

ax.legend(legend_rects, days)

ax.set_ylabel('Activation Frequency')
ax.set_xlabel('Hour of the Day (0 is midnight)')
ax.set_title(floor.capitalize() + " Floor Hour-By-Hour")
ax.set_xticks(ind+width)
ax.set_xticklabels(["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"], horizontalalignment='center')

plt.show()

