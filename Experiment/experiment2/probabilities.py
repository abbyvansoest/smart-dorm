# take in data from first_week, second_week, and third_week
# go through each file, categorize history for each sensor for every minute, updating at every minute interval
# based on categorization, increment counts 

import matplotlib.pyplot as plt
import numpy as np
import pylab


def get_dcg(sequence):
	dcg_ones = 0.0
	dcg_back = 0.0
	dcg_zeros = 0.0
	dcg_zeros_back = 0.0

	one_freq = 0
	zero_freq = 0

	for j in range(1,len(sequence)+1):
		i = len(sequence)+1 - j
		
		dcg_ones = dcg_ones + sequence[i-1]/float(j)
		dcg_back = dcg_back + sequence[j-1]/float(j)

		if (sequence[i-1] == 0):
			use1 = 1
		else:
			use1 = 0
		if (sequence[j-1] == 0):
			use2 = 1
		else:
			use2 = 0
		dcg_zeros = dcg_zeros + use1/float(j)
		dcg_zeros_back = dcg_zeros_back + use2/float(j)

		if (sequence[j-1]==1):
			one_freq = one_freq + 1
		else:
			zero_freq = zero_freq + 1

	if (one_freq == 0):
		diff1 = 0
	else:
		diff1 = dcg_ones/one_freq - dcg_back/one_freq
	if (zero_freq == 0):
		diff0 = 0
	else:
		diff0 = dcg_zeros/zero_freq - dcg_zeros_back/zero_freq 

	return diff1, diff0

# how many std deviations from the mean is this value
def stddev(average, history_length):
	if (history_length == 5):
		sd = .0993
		mean = .0000759 
	if (history_length == 10):
		sd = .0775
		mean = .0001
	if (history_length == 15):
		sd = 0.0657412560821
		mean = 5.19945496431e-05
		# or:
		# sd = 0.054582911188
		# mean = -2.02697717924e-05
	if (history_length == 20):
		sd = 0.0401660169834
		mean = -1.35369388876e-05
	if (history_length == 25):
		sd = 0.0313746923101
		mean = 9.12079000843e-06
	if (history_length == 30):
		sd = .02259
		mean = 0
	return (average - mean)/sd

def get_freq_thresholds(history_length):
	
	if (history_length == 5):
		return 0, .4, .8
	if (history_length == 10):
		return .1, .34, .67
	if (history_length == 15):
		return 0.07, 0.27, 0.47
	if (history_length == 20):
		return .1, .34, .67
	if (history_length == 30):
		return .134, .3, .634

def classify(history, hour, thresh):

	if (len(history) >= 45):
		hour = hour - 1
		if (hour == -1):
			hour = 23

	history_length = int((len(history)-5)/3)
	# classify history frequency
	LOW_FREQ = 0
	MID_LOW_FREQ = 1
	MID_HIGH_FREQ = 2
	HIGH_FREQ = 3 
	lower_thresh, middle_thresh, upper_thresh = get_freq_thresholds(history_length)

	span = .005

	# classify history trend over time
		# use partialization by 3 (not 2)
	UNKNOWN = -1
	STEADY = 0
	INCREASING = 1 
	DECREASING = 2

	hist1 = history[0:history_length]
	hist2 = history[history_length:2*history_length]
	hist3 = history[2*history_length:len(history)-5]
	future = history[len(history)-5:len(history)]

	# obtain frequencies for most recent history and two preceding
	freq1 = 0
	for item in hist1:
		thing = int(item)
		if thing == 1:
			freq1 = freq1 + 1
	freq2 = 0
	for item in hist2:
		thing = int(item)
		if thing == 1:
			freq2 = freq2 + 1
	freq3 = 0
	for item in hist3:
		thing = int(item)
		if thing == 1:
			freq3 = freq3 + 1

	# get ratios
	ratio1 = float(freq1) / float(history_length)
	ratio2 = float(freq2) / float(history_length)
	ratio3 = float(freq3) / float(history_length)


	frequency_class = -1

	# classify frequency
	if (ratio3 < lower_thresh):
		frequency_class = LOW_FREQ
	elif (ratio3 < middle_thresh):
		frequency_class = MID_LOW_FREQ
	elif (ratio3 < upper_thresh):
		frequency_class = MID_HIGH_FREQ
	else:
		frequency_class = HIGH_FREQ

	# classify trend over time
	# use dcg function 
	neg_thresh = 0.0 - thresh
	dcg1, dcg0 = get_dcg(hist3)
	avg = (dcg1 + dcg0)/2.0
	sd = stddev(avg,history_length)
	if (sd >= thresh):
		# which dcg is it in agreement with
		if (dcg1 > 0):
			trend = INCREASING
		elif(dcg0 > 0):
			trend = DECREASING
	elif (sd <= neg_thresh):
		if (dcg1 < 0):
			trend = DECREASING
		elif (dcg0 < 0):
			trend = INCREASING
	else:
		trend = STEADY

	onIn5 = 0
	for item in future:
		if item == 1:
			onIn5 = onIn5 + 1

	# if (frequency_class == LOW_FREQ and trend == STEADY and max(hist3)>0 and sd > .70):
	# 	print "dcg1 " + str(dcg1)
	# 	print "dcg0 " + str(dcg0)
	# 	print avg
	# 	print sd
	# 	print hist3
	# 	print future

	return frequency_class, trend, onIn5


def update_history(hist, track):
	hist.append(track)
	del hist[0]
	return hist

def getTime(timer):
	hour = int(timer / 60)
	hour = int(hour % 24)
	minutes = int(timer % 60)
	s_hour = str(hour)
	if hour < 10:
		s_hour = "0"+s_hour;
	s_min = str(minutes)
	if minutes < 10:
		s_min = "0"+s_min

	s = s_hour + ":" + s_min
	return s

# run full experiment on data
# parse through each line of the data, send to select policy 
def runExperiment(files, history_length, thresh):

	# classify history frequency
	LOW_FREQ = 0
	MID_LOW_FREQ = 1
	MID_HIGH_FREQ = 2
	HIGH_FREQ = 3 
	# classify history trend over time
		# use partialization by 3 (not 2)
	STEADY = 0
	INCREASING = 1 
	DECREASING = 2

	prob_table = [[0 for i in range(3)] for j in range(4)]
	freq_table = [[0 for i in range(3)] for j in range(4)]
	total_events = 0

	for datafile in files:

		datastream = open(datafile, "rw+")
		timer = history_length*3 + 5

		#  read in first line - has number of sensors being used
		num_sensors = int(datastream.readline())	

		#  for each line in the file (represents a minute), read in sensor information
		#  select a policy for each sensor
		#  update sensor-specifically
		entry = datastream.readline()
		# read in history_length lines and record history
		history = [[] for i in range(num_sensors)]
		for index in range(history_length*3 + 5):
			entry = datastream.readline()
			entry.replace("\n", "")
			entry_array = entry.split()
			for j in range(num_sensors):
				history[j].append(int(entry_array[j]))

		entry = datastream.readline()

		while (entry != ""):

			t = getTime(timer);

			if (entry == "\n"):
				break
			entry.replace("\n", "")
			entry_array = entry.split()

			# for each sensor
			for i in range(0,num_sensors):

				#  entry_array[i] = current activation status of sensor i
				#  policy = selected policy for sensor 
				#  time_left = time remaining in the contract for sensor i
				t_split = t.split(":")

				frequency_class, trend, onIn5 = classify(history[i], int(t_split[0]), thresh)
				total_events = total_events + 1

				if (onIn5 >= 1):
					prob_table[frequency_class][trend] = prob_table[frequency_class][trend] + 1
				freq_table[frequency_class][trend] = freq_table[frequency_class][trend] + 1
				#at each step, update history
				history[i] = update_history(history[i], int(entry_array[i]))

			timer = timer + 1
			entry = datastream.readline()

	for entry1 in range(4):
		for entry2 in range(3):
			
			if (freq_table[entry1][entry2] == 0):
				continue
			prob_table[entry1][entry2] = float(prob_table[entry1][entry2]) / float(freq_table[entry1][entry2])
	print prob_table
	return prob_table



history_length = 30

t1 = .9
files = ["experiment_data/first_week.txt", "experiment_data/second_week.txt", "experiment_data/third_week.txt"]
pt_t1 = runExperiment(files, history_length, t1)


t2 = .5
files = ["experiment_data/first_week.txt", "experiment_data/second_week.txt", "experiment_data/third_week.txt"]
pt_t2 = runExperiment(files, history_length, t2)


pc = [[0 for i in range(3)] for j in range(4)]
for entry1 in range(4):
	for entry2 in range(3):
		pc[entry1][entry2] = (pt_t1[entry1][entry2] - pt_t2[entry1][entry2])/pt_t2[entry1][entry2]
print pc
# graph 

STEADY = 0
INCREASING = 1
DECREASING = 2

import plotly.plotly as py
import plotly.graph_objs as go

py.sign_in('asoest', 'SGqWW58Ux3KD9Qa60z8O')

import plotly.tools as tls
tls.set_credentials_file(username='asoest', api_key='SGqWW58Ux3KD9Qa60z8O')

trace1 = go.Bar(
    x=['Low', 'Mid-Low', 'Mid-High', "High"],
    y=[pc[0][STEADY], pc[1][STEADY], pc[2][STEADY], pc[3][STEADY]],
    name='Steady'
)
trace2 = go.Bar(
    x=['Low', 'Mid-Low', 'Mid-High', "High"],
    y=[pc[0][INCREASING], pc[1][INCREASING], pc[2][INCREASING], pc[3][INCREASING]],
    name='Increasing'
)
trace3 = go.Bar(
    x=['Low', 'Mid-Low', 'Mid-High', "High"],
    y=[pc[0][DECREASING], pc[1][DECREASING], pc[2][DECREASING], pc[3][DECREASING]],
    name='Decreasing'
)

data = [trace1, trace2, trace3]
layout = go.Layout(
	title='Percent change in probability of activation from t = 0.5 to t = 0.9 \n history length = 20',
	barmode='group',
	xaxis=dict(
        title='Frequency Class',
        titlefont=dict(
            size=16,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Change in Probability of activation',
        titlefont=dict(
            size=16,
            color='#7f7f7f'
        )
    )
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='percchange_20')


