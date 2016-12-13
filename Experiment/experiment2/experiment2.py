
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

# calculate energy consumption by lights based on sensor activity
def calculate_energy(active_minutes):
	total_active = 0
	for num in active_minutes:
		total_active = total_active + num
		# energy consumed per minute by a light associated with a single sensor
	hours_active = float(total_active)/float(60)
	POWER = 11; 
	return float(POWER*hours_active)/float(1000.), total_active

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
	UNKNOWN = -1
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
	if (ratio3 < lower_thresh):
		frequency_class = LOW_FREQ
	elif (ratio3 < middle_thresh):
		frequency_class = MID_LOW_FREQ
	elif (ratio3 < upper_thresh):
		frequency_class = MID_HIGH_FREQ
	else:
		frequency_class = HIGH_FREQ

	# classify trend over time
	trend = UNKNOWN
	# increasing or decreasing if trend is strong enough over time
	if (ratio3 > ratio2+span and ratio2 >= ratio1+span):
		trend = INCREASING
	elif (ratio3 < ratio2-span and ratio2 <= ratio1-span):
		trend = DECREASING
	# steady if trends are minor enough over time
	elif (ratio3 < ratio2+span and ratio3 > ratio2 - span and ratio3 < ratio1+span and ratio3 > ratio1 - span):
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
def runExperiment(datafile, history_length, savename):

	rationame = "ratio_data/ratios"+str(history_length)+".txt"
	ratio_file = open(rationame, "w")

	# classify history frequency
	LOW_FREQ = 0
	MID_LOW_FREQ = 1
	MID_HIGH_FREQ = 2
	HIGH_FREQ = 3 

	# classify history trend over time
		# use partialization by 3 (not 2)
	UNKNOWN = -1
	STEADY = 0
	INCREASING = 1 
	DECREASING = 2

	LOW = 2
	HIGH = 15
	INCR = 1

	datastream = open(datafile, "rw+")
	timer = history_length*3
	num_turn_on = 0
	num_expired = 0
	num_mid_renew = 0
	num_leave_off = 0
	num_wasted_mins = 0

	all_policy_actions = open(savename, "w")

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

	total_events = 0

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
			ratio_file.write(str(ratio3)+"\n")
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
			if (trend == UNKNOWN):
				t_str = "UNKNOWN"
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

				elif (trend == STEADY or trend == UNKNOWN):
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

				elif (trend == STEADY or trend == UNKNOWN):
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

				elif (trend == STEADY or trend == UNKNOWN):
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

				elif (trend == STEADY or trend == UNKNOWN):
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

			all_policy_actions.write(t + "\t" + str(entry_array[i]) + "\t" + str(timeInPolicy[i]) + "\t" + str(length_of_policy[i]) + "\t" + fc_str + ", "+t_str + "\n")

		timer = timer + 1
		entry = datastream.readline()

	energy, total_active = calculate_energy(active_minutes)
	print energy
	name = savename.split(".")
	fo = open(name[0]+"_summary.txt", "w")
	
	fo.write("ENERGY USAGE: " + str(energy) + "\n")
	fo.write("number of active minutes: " + str(total_active) +"\n")
	fo.write("number of occupancy events: " + str(total_events) + "\n")
	fo.write("number of wasted minutes: " + str(num_wasted_mins) + "\n")
	fo.write("number contracts renewed in middle: " + str(num_mid_renew) + "\n")
	fo.write("number contracts created from nothing: " + str(num_turn_on) + "\n")
	all_policy_actions.close()
	fo.close()


### generate all data files ###


hist_length = 10

filename = "experiment_data/first_week.txt"
savename = "improve_classify/policy/hist10_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "improve_classify/policy/hist10_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "improve_classify/policy/hist10_third.txt"
runExperiment(filename, hist_length, savename)


hist_length = 15

filename = "experiment_data/first_week.txt"
savename = "improve_classify/policy/hist15_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "improve_classify/policy/hist15_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "improve_classify/policy/hist15_third.txt"
runExperiment(filename, hist_length, savename)


hist_length = 20

filename = "experiment_data/first_week.txt"
savename = "improve_classify/policy/hist20_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "improve_classify/policy/hist20_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "improve_classify/policy/hist20_third.txt"
runExperiment(filename, hist_length, savename)


hist_length = 30

filename = "experiment_data/first_week.txt"
savename = "improve_classify/policy/hist30_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "improve_classify/policy/hist30_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "improve_classify/policy/hist30_third.txt"
runExperiment(filename, hist_length, savename)











