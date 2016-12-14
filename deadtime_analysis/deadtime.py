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
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go

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

threshold = 150
count = [0 for i in range(threshold+1)]
mypath = 'data/week/'
dest_dir = 'hists/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

if '.DS_Store' in files: files.remove('.DS_Store')

cumulative = [0] * threshold

# Open each file and run to develop a histogram
# for f in files:
# 	name, extension = os.path.splitext(f)
# 	fo = open(mypath+f, "rw+")

# 	mins_between = [] # vector for all time diffs

# 	prev_entry = fo.readline() # first active time to init things
# 	first_vals = prev_entry.split("\t")
# 	prev_time = first_vals[0]

# 	# read in all data and record time differences between activation
# 	entry = fo.readline()
# 	max_diff = -1

# 	while (entry != ""):
# 		values = entry.split("\t")
# 		cur_time = values[0]
# 		cur_status = int(values[1])

# 		if (cur_time == prev_time):
# 			entry = fo.readline()
# 			continue

# 		if (cur_status == 1):
# 			time_diff = calculate_time_diff(prev_time, cur_time)
# 			if (time_diff > max_diff):
# 				max_diff = time_diff
# 			if (time_diff <= threshold):
# 				mins_between.append(time_diff)
# 				count[time_diff] = count[time_diff] + 1
# 			prev_time = cur_time

# 		entry = fo.readline()

# 	fig = plt.figure()
# 	n, bins, patches = plt.hist(mins_between, bins=range(0, threshold+1,1), normed=True, color='b')
# 	save_name = dest_dir + name + '_2' + '.png'
# 	plt.title(name + ' Sensor, Dead Time Frequency')
# 	plt.xlabel('Time Since Last Activation')
# 	plt.ylabel('Frequency')
# 	plt.savefig(save_name)
# 	#plt.show()

# 	num = get_counts(mins_between, threshold)
# 	cumulative = map(add, cumulative, num)
# 	print cumulative


cumulative = [0, 9638, 6979, 3534, 2141, 1431, 996, 724, 611, 445, 322, 327, 256, 204, 186, 176, 160, 146, 130, 115, 91, 70, 58, 74, 68, 47, 53, 34, 49, 43, 44, 34, 22, 41, 34, 27, 21, 29, 17, 21, 20, 27, 23, 18, 18, 14, 13, 18, 18, 15, 16, 14, 22, 4, 9, 11, 10, 13, 9, 10, 8, 7, 10, 7, 6, 10, 4, 4, 12, 1, 6, 7, 10, 4, 7, 6, 3, 4, 2, 5, 0, 4, 9, 0, 0, 0, 2, 0, 2, 3, 0, 2, 2, 0, 1, 1, 1, 0, 1, 3, 1, 1, 0, 0, 0, 0, 1, 0, 0, 2, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 3, 3, 1, 1, 0, 0, 0, 0, 1, 0, 2, 2, 2, 3, 1, 1, 0, 1, 1, 1, 2, 1, 1, 1, 3, 1, 0, 0]
sum_cum = sum(cumulative)

for c in range(len(cumulative)):
	cumulative[c] = float(cumulative[c]) / float(sum_cum)

print cumulative

index = np.arange(threshold+1)

trace = go.Scatter(
    x = index,
    y = cumulative,
    mode = 'lines',
    name = 'lines'
)


py.sign_in('asoest', 'SGqWW58Ux3KD9Qa60z8O')

layout = go.Layout(
	title='Frequency of Time Between Sensor Events',
	barmode='group',
	xaxis=dict(
        title='Time Between Activations (Minutes)',
        titlefont=dict(
            size=16,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Frequency',
        titlefont=dict(
            size=16,
            color='#7f7f7f'
        )
    )
)

data = [trace]
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='deadtime_lines')
print cumulative
# fig, ax = plt.subplots()

# index = np.arange(threshold+1)
# bar_width = 0.5
# rects1 = plt.bar(index, cumulative, bar_width, color='b')
# plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E'))
# #n, bins, patches = plt.hist(cumulative, bins=range(0, threshold+1,1), normed=True)
# plt.title('Dead Time Frequency Over All Sensors') 
# plt.xlabel('Time Since Last Activation')
# plt.ylabel('Frequency')
# save_name = 'global_before_school' +'.png'
# plt.savefig(save_name)
# plt.show() 


# CUMuLATIVE DATA
#[0.0, 0.3223842654535724, 0.23344260101685843, 0.1182097939523682, 0.07161493176344662, 0.04786593524217286, 0.03331549371153331, 0.024217286593524217, 0.020437516724645437, 0.014884934439389885, 0.01077067166176077, 0.010937918116135937, 0.008563018464008563, 0.006823655338506824, 0.006221568102756221, 0.005887075194005887, 0.005351886540005352, 0.004883596467754884, 0.004348407813754348, 0.003846668450628847, 0.003043885469628044, 0.0023414503612523415, 0.00194005887075194, 0.0024752475247524753, 0.0022745517795022745, 0.0015721166711265722, 0.0017728124163767728, 0.0011372758897511372, 0.001639015252876639, 0.0014383195076264382, 0.0014717687985014718, 0.0011372758897511372, 0.0007358843992507359, 0.0013714209258763714, 0.0011372758897511372, 0.0009031308536259032, 0.0007024351083757025, 0.00097002943537597, 0.0005686379448755686, 0.0007024351083757025, 0.000668985817500669, 0.0009031308536259032, 0.0007693336901257693, 0.000602087235750602, 0.000602087235750602, 0.0004682900722504683, 0.0004348407813754348, 0.000602087235750602, 0.000602087235750602, 0.0005017393631255017, 0.0005351886540005352, 0.0004682900722504683, 0.0007358843992507359, 0.0001337971635001338, 0.000301043617875301, 0.00036794219962536795, 0.0003344929087503345, 0.0004348407813754348, 0.000301043617875301, 0.0003344929087503345, 0.0002675943270002676, 0.00023414503612523415, 0.0003344929087503345, 0.00023414503612523415, 0.0002006957452502007, 0.0003344929087503345, 0.0001337971635001338, 0.0001337971635001338, 0.0004013914905004014, 3.344929087503345e-05, 0.0002006957452502007, 0.00023414503612523415, 0.0003344929087503345, 0.0001337971635001338, 0.00023414503612523415, 0.0002006957452502007, 0.00010034787262510035, 0.0001337971635001338, 6.68985817500669e-05, 0.00016724645437516726, 0.0, 0.0001337971635001338, 0.000301043617875301, 0.0, 0.0, 0.0, 6.68985817500669e-05, 0.0, 6.68985817500669e-05, 0.00010034787262510035, 0.0, 6.68985817500669e-05, 6.68985817500669e-05, 0.0, 3.344929087503345e-05, 3.344929087503345e-05, 3.344929087503345e-05, 0.0, 3.344929087503345e-05, 0.00010034787262510035, 3.344929087503345e-05, 3.344929087503345e-05, 0.0, 0.0, 0.0, 0.0, 3.344929087503345e-05, 0.0, 0.0, 6.68985817500669e-05, 0.0, 3.344929087503345e-05, 3.344929087503345e-05, 0.0, 0.0, 3.344929087503345e-05, 0.0, 0.0, 0.0, 0.0, 3.344929087503345e-05, 3.344929087503345e-05, 0.00010034787262510035, 0.00010034787262510035, 3.344929087503345e-05, 3.344929087503345e-05, 0.0, 0.0, 0.0, 0.0, 3.344929087503345e-05, 0.0, 6.68985817500669e-05, 6.68985817500669e-05, 6.68985817500669e-05, 0.00010034787262510035, 3.344929087503345e-05, 3.344929087503345e-05, 0.0, 3.344929087503345e-05, 3.344929087503345e-05, 3.344929087503345e-05, 6.68985817500669e-05, 3.344929087503345e-05, 3.344929087503345e-05, 3.344929087503345e-05, 0.00010034787262510035, 3.344929087503345e-05, 0.0, 0.0]
