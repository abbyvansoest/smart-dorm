
# now for classification of history, also want to take in day and time of day
# use frequency data from average hours / minutes to change how we classify a given chunk of time

# that is, if it is a typically low frequency hour and you get a couple of activations, you don't want
# to hike up the active time very much (unless its REALLY active)

# and if you're in a high frequency hour, you probably want to do a little bit more (like be a bit more
# willing to add on to the length of activation becuase then you're likely to be ON for more people)


# now passign matrix of history arrays 6 x history_length
# classifying each
# making decision based off that
# try feeding only direct neighbors history data, only same-floor data, different floors data 

# use global average? of ratios etc.

import math

# calculate energy consumption by lights based on sensor activity
def calculate_energy(active_minutes):
	total_active = 0
	for num in active_minutes:
		total_active = total_active + num
		# energy consumed per minute by a light associated with a single sensor
	hours_active = float(total_active)/float(60)
	POWER = 11; 
	return float(POWER*hours_active)/float(1000), total_active

def get_dcg(sequence):
	dcg_ones = 0.0
	dcg_back = 0.0
	dcg_zeros = 0.0
	dcg_zeros_back = 0.0

	one_freq = 0
	zero_freq = 0

	for j in range(1,len(sequence)+1):
		i = len(sequence)+1 - j
		
		dcg_ones = dcg_ones + sequence[i-1]/math.log(j+1,2)#float(j)
		dcg_back = dcg_back + sequence[j-1]/math.log(j+1,2)#float(j)

		if (sequence[i-1] == 0):
			use1 = 1
		else:
			use1 = 0
		if (sequence[j-1] == 0):
			use2 = 1
		else:
			use2 = 0
		dcg_zeros = dcg_zeros + use1/math.log(j+1,2)#float(j)
		dcg_zeros_back = dcg_zeros_back + use2/math.log(j+1,2)#float(j)

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
# how many std deviations from the mean is this value
def stddev(average, history_length):
	if (history_length == 1):
		sd = 0.0
		mean = 0.0
	if (history_length == 2):
		sd = 0.0
		mean  = 0.0
	if (history_length == 3):
		sd = 0.0809938255361
		mean = 1.5e-05
	if (history_length == 4):
		sd = 0.0961955026187
		mean = -0.000136777385827
	if (history_length == 5):
		sd = 0.0991314934364
		mean = -5.16671883027e-05
	if (history_length == 6):
		sd = 0.0975201816914
		mean = -0.000251712503554
	if (history_length == 7):
		sd = 0.0935313474135
		mean = 1.67752463058e-06
	if (history_length == 8):
		sd = 0.0884527721142
		mean = 0.000254107357486
	if (history_length == 9):
		sd = 0.0830783710554
		mean = -9.23926211925e-06
	if (history_length == 10):
		sd = 0.0775383249301
		mean = -0.000118885387975
	if (history_length == 11):
		sd = 0.0721888314741
		mean = 3.78533062958e-05
	if (history_length == 12):
		sd = 0.0669610977087
		mean = -8.30047433629e-05
	if (history_length == 13):
		sd = 0.0625656384325
		mean = -1.57826377231e-05
	if (history_length == 14):
		sd = 0.0582614782236
		mean = 5.38984955053e-05
	if (history_length == 15):
		sd = 0.0544770223494
		mean = -2.05930337567e-05
	if (history_length == 16):
		sd = 0.0512090908314
		mean = 4.12208443227e-06
	if (history_length == 17):
		sd = 0.0479263341674
		mean = -4.78127371033e-05
	if (history_length == 18):
		sd = 0.0450099524507
		mean = -1.02161159482e-05
	if (history_length == 19):
		sd = 0.0425118870589
		mean = 5.05817768514e-08
	if (history_length == 20):
		sd = 0.0400840002389
		mean = -6.36434390678e-06
	if (history_length == 21):
		sd = 0.0380649559586
		mean = 4.3819497073e-06
	if (history_length == 22):
		sd = 0.0362082708024
		mean = 1.84184993387e-05
	if (history_length == 23):
		sd = 0.034468368055
		mean = 1.86137334364e-05
	if (history_length == 24):
		sd = 0.0328433535662
		mean = -1.8989803463e-05
	if (history_length == 25):
		sd = 0.031436587224
		mean = -1.22836515379e-07
	if (history_length == 26):
		sd = 0.0301499822855
		mean = 2.67411130777e-05
	if (history_length == 27):
		sd = 0.0289383947815
		mean = 2.28163005556e-06
	if (history_length == 28):
		sd = 0.0278922168051
		mean = 7.28719138835e-06
	if (history_length == 29):
		sd = 0.0268419016853
		mean = 3.15668748045e-05
	if (history_length == 30):
		sd = 0.0259132856735
		mean = 4.34097434428e-05
	return (average - mean)/sd

def get_freq_thresholds(history_length):

	if (history_length == 5 or history_length == 6 or history_length == 4 or history_length == 3):
		return 0, .4, .8
	if (history_length == 7 or history_length == 8):
		return 0, .25, .75
	if (history_length == 10 or history_length == 11 or history_length == 9):
		return .1, .34, .67
	if (history_length == 14 or history_length == 13 or history_length == 12):
		return .15, .36, .65
	if (history_length == 15 or history_length == 16 or history_length == 17):
		return 0.07, 0.27, 0.48
	if (history_length == 20 or history_length == 21 or history_length == 22 or history_length == 19 or history_length == 18):
		return .1, .34, .67
	if (history_length == 25 or history_length == 26 or history_length == 24 or history_length == 23):
		return .12, .36, .625
	if (history_length == 30 or history_length == 29 or history_length == 28 or history_length == 27):
		return .134, .3, .634
	
def classify(history, hour):

	if (len(history) >= 45):
		hour = hour - 1
		if (hour == -1):
			hour = 23

	history_length = int(len(history)/3)
	# classify history frequency
	LOW_FREQ = 0
	MID_LOW_FREQ = 1
	MID_HIGH_FREQ = 2
	HIGH_FREQ = 3 
	lower_thresh, middle_thresh, upper_thresh = get_freq_thresholds(history_length)

	span = .005

	# classify history trend over time
		# use partialization by 3 (not 2)
	STEADY = 0
	INCREASING = 1 
	DECREASING = 2

	hist1 = history[0:history_length]
	hist2 = history[history_length:2*history_length]
	hist3 = history[2*history_length:len(history)]

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
	if (ratio3 <= lower_thresh):
		frequency_class = LOW_FREQ
	elif (ratio3 <= middle_thresh):
		frequency_class = MID_LOW_FREQ
	elif (ratio3 <= upper_thresh):
		frequency_class = MID_HIGH_FREQ
	else:
		frequency_class = HIGH_FREQ

	# classify trend over time
	# use dcg function 
	thresh = .75
	neg_thresh = -.75
	dcg1, dcg0 = get_dcg(hist3)
	avg = (dcg1 + dcg0)/2.0
	sd = stddev(avg, history_length)
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

	return frequency_class, trend, ratio3


def update_history(hist, track):
	size = len(track)
	history = hist + track
	del history[0:size]
	return history

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
def runExperiment(datafile, history_length):

	# rationame = "ratio_data/ratios"+str(history_length)+".txt"
	# ratio_file = open(rationame, "w")

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

	datastream = open(datafile, "rw+")
	timer = history_length*3
	num_turn_on = 0
	num_expired = 0
	num_mid_renew = 0
	num_leave_off = 0
	num_wasted_mins = 0
	total_events = 0

	#  read in first line - has number of sensors being used
	num_sensors = int(datastream.readline())	
	timeInPolicy = [0] * num_sensors
	active_minutes = [0] * num_sensors 
	length_of_policy = [0] * num_sensors

	#  for each line in the file (represents a minute), read in sensor information
	#  select a policy for each sensor
	#  update sensor-specifically
	entry = datastream.readline()
	# read in history_length lines and record history
	history = [[] for i in range(num_sensors)]
	for index in range(history_length*3):
		entry = datastream.readline()
		entry.replace("\n", "")
		entry_array = entry.split()
		for j in range(num_sensors):
			history[j].append(int(entry_array[j]))
	# history tracking list for each sensor
	track = [[] for k in range(num_sensors)]


	entry = datastream.readline()

	while (entry != ""):

		t = getTime(timer);

		if (entry == "\n"):
			break
		entry.replace("\n", "")
		entry_array = entry.split()

		# for each sensor
		for i in range(0,num_sensors):

		#	print "i: " + str(i)
			if (len(entry_array) != num_sensors):
				print "ERROR"
				break

			#  entry_array[i] = current activation status of sensor i
			#  policy = selected policy for sensor 
			#  time_left = time remaining in the contract for sensor i
			t_split = t.split(":")

			frequency_class, trend, ratio3 = classify(history[i], int(t_split[0]))
			#ratio_file.write(str(ratio3)+"\n")
			fc_str = ""
			t_str = ""
			if (frequency_class == LOW_FREQ):
				fc_str = "LOW"
			if (frequency_class == MID_LOW_FREQ):
				fc_str = "MID LOW"
			if (frequency_class == MID_HIGH_FREQ):
				fc_str = "MID HIGH"
			if (frequency_class == HIGH_FREQ):
				fc_str = "HIGH"
			if (trend == INCREASING):
				t_str = "INCREASING"
			if (trend == DECREASING):
				t_str = "DECREASING"
			if (trend == STEADY):
				t_str = "STEADY"
			#print fc_str + ", "+ t_str

			time_left = timeInPolicy[i]
			in_policy = False
			if (time_left > 0):
				in_policy = True

			if (frequency_class == LOW_FREQ):
				if (trend == INCREASING):
					length_of_policy[i] = 3
					if (int(entry_array[i]) == 1):
						if (in_policy):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = length_of_policy[i]
					elif (int(entry_array[i]) == 0):
						if (time_left > 0):
							timeInPolicy[i] = time_left - 1

				elif (trend == DECREASING):
					length_of_policy[i] = 2
					if (int(entry_array[i]) == 1):
						if (in_policy):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = length_of_policy[i]
					elif (int(entry_array[i]) == 0):
						if (time_left == 1):
							timeInPolicy[i] = 0
						elif (time_left > 1):
							timeInPolicy[i] = 1

				elif (trend == STEADY):
					length_of_policy[i] = 1
					if (int(entry_array[i]) == 1):
						if (in_policy):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = length_of_policy[i]
					elif (int(entry_array[i]) == 0):
						if (time_left > 0):
							timeInPolicy[i] = timeInPolicy[i] - 1

			if (frequency_class == MID_LOW_FREQ):
				if (trend == INCREASING):
					length_of_policy[i] = 6
					if (int(entry_array[i]) == 1):
						if (in_policy):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = length_of_policy[i]
					elif (int(entry_array[i]) == 0):
						if (time_left > 0):
							timeInPolicy[i] = time_left - 1
							
				elif (trend == DECREASING):
					length_of_policy[i] = 4
					if (int(entry_array[i]) == 1):
						if (in_policy):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = length_of_policy[i]
					elif (int(entry_array[i]) == 0):
						if (time_left == 1):
							timeInPolicy[i] = 0
						elif (time_left > 1):
							timeInPolicy[i] = time_left - 2

				elif (trend == STEADY):
					length_of_policy[i] == 5
					if (int(entry_array[i]) == 1):
						if (in_policy):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = length_of_policy[i]
					elif (int(entry_array[i]) == 0):
						if (time_left > 0):
							timeInPolicy[i] = time_left - 1

			if (frequency_class == MID_HIGH_FREQ):
				if (trend == INCREASING):
					length_of_policy[i] = 9
					if (int(entry_array[i]) == 1):
						if (in_policy and time_left > length_of_policy[i] - 5):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = time_left + 5
					elif (int(entry_array[i]) == 0):
						if (timeInPolicy[i] > 0):
							timeInPolicy[i] = timeInPolicy[i] - 1

				elif (trend == DECREASING):
					length_of_policy[i] = 7
					if (int(entry_array[i]) == 1):
						if (in_policy):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = length_of_policy[i]
					elif (int(entry_array[i]) == 0):
						if (timeInPolicy[i] > 0):
							timeInPolicy[i] = timeInPolicy[i] - 1

				elif (trend == STEADY):
					length_of_policy[i] = 8
					if (int(entry_array[i]) == 1):
						if (in_policy):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = length_of_policy[i]
					elif (int(entry_array[i]) == 0):
						if (timeInPolicy[i] > 0):
							timeInPolicy[i] = timeInPolicy[i] - 1

			if (frequency_class == HIGH_FREQ):
				if (trend == INCREASING):
					length_of_policy[i] = 10
					if (int(entry_array[i]) == 1):
						if (in_policy):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = length_of_policy[i]
					elif (int(entry_array[i]) == 0):
						if (timeInPolicy[i] > 0):
							timeInPolicy[i] = timeInPolicy[i] - 1

				elif (trend == DECREASING):
					length_of_policy[i] = 8
					if (int(entry_array[i]) == 1):
						if (in_policy):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = length_of_policy[i]
					elif (int(entry_array[i]) == 0):
						if (timeInPolicy[i] > 0):
							timeInPolicy[i] = timeInPolicy[i] - 1

				elif (trend == STEADY):
					length_of_policy[i] = 9
					if (int(entry_array[i]) == 1):
						if (in_policy):
							timeInPolicy[i] = time_left
						else:
							timeInPolicy[i] = length_of_policy[i]
					elif (int(entry_array[i]) == 0):
						if (timeInPolicy[i] > 0):
							timeInPolicy[i] = timeInPolicy[i] - 1

			## calculate energy consumption for given miunte
			if (timeInPolicy[i] > 0):
				# using_energy tracks the number of minutes single sensors are active
				# i.e. if 4 sensors are active in a given minute, the var increases by 4
				# then, each sensor activates a light that uses a given amount of energy per minute
				# multiply final value of using_energy by this amount of energy
				active_minutes[i] = active_minutes[i] + 1 
			if (time_left == 0 and timeInPolicy[i] > 0):
				num_turn_on = num_turn_on + 1
			if (int(entry_array[i]) == 1 and time_left > 0):
				num_mid_renew = num_mid_renew + 1
			if (int(entry_array[i]) == 0 and time_left > 0):
				num_wasted_mins = num_wasted_mins + 1
			if (int(entry_array[i]) == 1):
				total_events = total_events + 1

			# if have built up enough history, update history
			if (len(track[i]) == history_length):
				history[i] = update_history(history[i], track[i])
				track[i] = []
				track[i].append(int(entry_array[i]))
			else:
				track[i].append(int(entry_array[i]))

		timer = timer + 1
		entry = datastream.readline()


	energy, total_active = calculate_energy(active_minutes)

	return total_active, num_wasted_mins, total_events, num_mid_renew


### generate all data files ###

span = 30

filename = "experiment_data/first_week.txt"
outfile = "dcg/first_span.txt"
f_out = open(outfile, "w")
# for all history lengths up to an including span
for i in range(3,span+1):
	active, wasted, events, renewed = runExperiment(filename, i)
	print active
	print wasted
	print events
	print renewed
	f_out.write(str(i)+ ": \n")
	f_out.write(str(active)+"\n")
	f_out.write(str(wasted)+"\n")
	f_out.write(str(events)+"\n")
	f_out.write(str(renewed)+"\n")

f_out.close()


filename = "experiment_data/second_week.txt"
outfile = "dcg/second_span.txt"
f_out = open(outfile, "w")
# for all history lengths up to an including span
for i in range(3,span+1):
	active, wasted, events, renewed = runExperiment(filename, i)
	print active
	print wasted
	print events
	print renewed
	f_out.write(str(i)+ ": \n")
	f_out.write(str(active)+"\n")
	f_out.write(str(wasted)+"\n")
	f_out.write(str(events)+"\n")
	f_out.write(str(renewed)+"\n")
f_out.close()


filename = "experiment_data/third_week.txt"
outfile = "dcg/third_span.txt"
f_out = open(outfile, "w")
# for all history lengths up to an including span
for i in range(3,span+1):
	active, wasted, events, renewed = runExperiment(filename, i)
	print active
	print wasted
	print events
	print renewed
	f_out.write(str(i)+ ": \n")
	f_out.write(str(active)+"\n")
	f_out.write(str(wasted)+"\n")
	f_out.write(str(events)+"\n")
	f_out.write(str(renewed)+"\n")

f_out.close()
	



