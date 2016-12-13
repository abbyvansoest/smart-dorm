
# now for classification of history, also want to take in day and time of day
# use frequency data from average hours / minutes to change how we classify a given chunk of time

# that is, if it is a typically low frequency hour and you get a couple of activations, you don't want
# to hike up the active time very much (unless its REALLY active)

# and if you're in a high frequency hour, you probably want to do a little bit more (like be a bit more
# willing to add on to the length of activation becuase then you're likely to be ON for more people)

# based on the hour, return the average ratio for the hour
def get_avg_ratio(hour):
	ratios = [0.2253968253968254, 0.1728835978835979, 0.09656084656084656, 0.06349206349206349, 0.037698412698412696, 0.028042328042328042, 0.06402116402116402, 0.11812169312169313, 0.1689153439153439, 0.17314814814814813, 0.18029100529100528, 0.14854497354497354, 0.19642857142857142, 0.1873015873015873, 0.1585978835978836, 0.14775132275132274, 0.20582010582010582, 0.20515873015873015, 0.17314814814814813, 0.21851851851851853, 0.24404761904761904, 0.24193121693121694, 0.26521164021164023, 0.24259259259259258]
	return ratios[hour]	

# calculate energy consumption by lights based on sensor activity
def calculate_energy(active_minutes):

	hours_active = float(active_minutes)/float(60)
	POWER = 11; 
	return float(POWER*hours_active)/float(1000.)

def classify(history, hour):

	if (len(history) >= 45):
		hour = hour - 1
		if (hour == -1):
			hour = 23

	# classify history of length history_length based on criteria
	LOW_FREQ = 0
	INCREASING = 1 
	DECREASING = 2
	HIGH_FREQ = 3
	MID_FREQ = 4

	increment = float(1)/float(20)
	upper_threshold = 17
	lower_threshold = 2

	history_length = len(history)
	half_len = int(history_length/2)
	hist1 = history[0:half_len]
	hist2 = history[half_len:len(history)+1]

	# obtain frequencies for each half of history
	# and for the full history
	freq = 0
	for item in history:
		thing = int(item)
		if thing == 1:
			freq = freq + 1
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

	# classify freq1 in zone 1 through N
	check = 0
	ratio1 = float(freq1) / float(half_len)
	zone1 = 0
	while (check < 1):
		if (ratio1 > check):
			zone1 = zone1 + 1
		elif (ratio1 <= check):
			break
		check = check + increment
	
	# classify freq2 in zone 1 through N
	check = 0
	ratio2 = float(freq2) / float(half_len)
	zone2 = 0
	while (check < 1):
		if (ratio2 > check):
			zone2 = zone2 + 1
		elif (ratio2 <= check):
			break
		check = check + increment

	# get the stored average ratio for the hour
		# that is, avg freq / 60
	# classify avg_ratio in zone 1 through N
	avg_ratio = get_avg_ratio(hour)
	# print "hour: " + str(hour) + "  " + "avg_ratio: "+ str(avg_ratio)
	# print "ratio 1: "+ str(ratio1)
	# print "ratio 2: "+ str(ratio2)
	check = 0
	zone_avg = 0
	while (check < 1):
		if (avg_ratio > check):
			zone_avg = zone_avg + 1
		elif (avg_ratio <= check):
			break
		check = check + increment

	# if the average zone for this hour is very low, 
	if (avg_ratio < .065):
		# force low freq
		return LOW_FREQ, 1, True

	# print str(zone1) + " " + str(zone2) + " " + str(zone_avg)
	# print "*******************"
	# print "\n"
	# take care of bad / outlying situations
	# protect from increasing drastically in low freq times 
		# and decreasing drastically in high freq times
	dist_from_avg = 2
	diff_threshold = 2
	small_adjust = 2
	edited = False
	# too low and decreasing
	if (zone1 < zone_avg - dist_from_avg and zone2 < zone1):
		edited = True
		# override to keep at current level, if outside a given range of difference
		# do nothing if the difference between 1 and 2 is less than 5
		if (zone1 - zone2 < diff_threshold):
			if (zone_avg - zone1 > 3):
				return INCREASING, small_adjust, edited
			else:
				return MID_FREQ, 0, edited
		# if the difference is greater than 5, adjust by 1 (or other small number)
		else:
			return DECREASING, small_adjust, edited

	# too high and increasing
	if (zone1 > zone_avg + dist_from_avg and zone2 > zone1):
		edited = True
		# override to keep at current level, if outside a given range of difference 
		# do nothing if the difference between 1 and 2 is less than 5
		if (zone2 - zone1 < diff_threshold):
			# if difference between 1 and 2 is small but difference to average is big, adjust a bit
			if (zone1 - zone_avg > 3):
				return INCREASING, small_adjust, edited
			else:
				return MID_FREQ, 0, edited

		# if the difference is greater than 5, adjust by 1 (or other small number)
		else:
			return INCREASING, small_adjust, edited

	# right on, low, and increasing
	if (zone1 == zone_avg and zone2 > zone1 and zone_avg <= lower_threshold):
		edited = True
		# if outside a given range of difference, increase by 1
		if (zone2 > zone1 + 1):
			return INCREASING, 1, edited
		# otherwise keep at current level
		else:
			return MID_FREQ, 0, edited

	# right on, high, and decreasing
	if (zone1 == zone_avg and zone2 < zone1 and zone_avg >= upper_threshold):
		edited = True
		# if outside a given range of difference, decrease by 1
		if (zone2 < zone1 - 1):
			return DECREASING, 1, edited
		# otherwise keep at current level
		else:
			return MID_FREQ, 0, edited

	# compare the zones that the first and second halfs of the history were placed in
	# if in the same zone, maintain current activation policy
	# if X zones up/down, increase/decrease by X minutes
	compare = zone2 - zone1
	if (compare == 0):
		return MID_FREQ, 0, edited
	if (compare < 0):
		return DECREASING, abs(compare), edited
	if (compare > 0):
		return INCREASING, compare, edited

	return -1

def update_history(hist, next):
	history = hist
	history.append(next)
	del history[0]
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

	LOW_FREQ = 0
	INCREASING = 1 
	DECREASING = 2
	HIGH_FREQ = 3
	MID_FREQ = 4

	LOW = 2
	HIGH = 15
	INCR = 1

	# energy consumed per minute by a light associated with a single sensor
	ENG_CONSUMED_PER_MIN = 11; 

	datastream = open(datafile, "rw+")
	timer = history_length
	num_turn_on = 0
	num_expired = 0
	num_mid_renew = 0
	num_leave_off = 0
	num_changes = 0
	num_wasted_mins = 0

	all_policy_actions = open(savename, "w")

	#  read in first line - has number of sensors being used
	num_sensors = int(datastream.readline())	
	timeInPolicy = [0] * num_sensors

	#  for each line in the file (represents a minute), read in sensor information
	#  select a policy for each sensor
	#  update sensor-specifically
	entry = datastream.readline()
	# read in history_length lines and record history
	history = [[] for i in range(num_sensors)]
	for i in range(history_length):
		entry = datastream.readline()
		entry.replace("\n", "")
		entry_array = entry.split()
		for j in range(num_sensors):
			history[j].append(entry_array[j])

	active_minutes = 0
	total_events = 0

	stored_classifications = [-1] * num_sensors
	length_of_policy = [0] * num_sensors
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

			#print entry_array[i]
			#  entry_array[i] = current activation status of sensor i
			#  policy = selected policy for sensor 
			#  time_left = time remaining in the contract for sensor i
			prev_classify = stored_classifications[i]
			t_split = t.split(":")
			classification, diff, edited = classify(history[i], int(t_split[0]))
			increment = diff * 1
			change = False
			if (prev_classify != classification):
				stored_classifications[i] = classification
				change = True
				num_changes = num_changes + 1
			time_left = timeInPolicy[i]
			action = ""
			cl = ""
			# use classification to decide settings
			if (classification == LOW_FREQ):
				# set policy to turn off immediately - no time left
				# if activated in this minute, turn on only for LOW minutes
				length_of_policy[i] = LOW
				cl = "LOW"

			if (classification == INCREASING):
				# increase time being added to policy renewal based on frequency/distribution data
				if (length_of_policy[i] + increment < HIGH):
					length_of_policy[i] = length_of_policy[i] + increment
				else:
					length_of_policy[i] = HIGH
				cl = "INCREASING"

			if (classification == DECREASING):
				# decrease time being added to policy renewal based on frequency/distribution data
				if (length_of_policy[i] - increment > 0):
					length_of_policy[i] = length_of_policy[i] - increment
				else:
					length_of_policy[i] = 0
				cl = "DECREASING"

			if (classification == HIGH_FREQ):
				# set policy to turn on for HIGH minutes whenever activated
				length_of_policy[i] = HIGH
				cl = "HIGH"
			if (classification == MID_FREQ):
				cl = "maintain"

			# handle current status update
			if (int(entry_array[i]) == 1):
				total_events = total_events + 1
				if (time_left >= 1):
					action = "CONTRACT RENEWED"
					num_mid_renew = num_mid_renew + 1
				elif (time_left == 0):
					action = "TURN ON"
					num_turn_on = num_turn_on + 1

				if (timeInPolicy[i] == 0):
					timeInPolicy[i] = length_of_policy[i]
				elif (timeInPolicy[i] > 0):
					# if in policy, extend by a non-full amount of time
					if (timeInPolicy[i] >= 15):
						timeInPolicy[i] = timeInPolicy[i] - 1
					elif (classification == INCREASING or classification == HIGH):
						timeInPolicy[i] = timeInPolicy[i] + 5
					else:
						timeInPolicy[i] = timeInPolicy[i]

			elif (int(entry_array[i]) == 0):
				if (time_left == 1):
					action = "LET EXPIRE"
					num_expired = num_expired + 1
				elif (time_left > 0):
					action = "WAIT LIFESPAN"
					num_wasted_mins = num_wasted_mins + 1
				elif (time_left == 0):
					action = "LEAVE OFF"
					num_leave_off = num_leave_off + 1
				if (timeInPolicy[i] > 0):
					timeInPolicy[i] = timeInPolicy[i] - 1

			## calculate energy consumption for given miunte
			if (timeInPolicy[i] > 0):
				# using_energy tracks the number of minutes single sensors are active
				# i.e. if 4 sensors are active in a given minute, the var increases by 4
				# then, each sensor activates a light that uses a given amount of energy per minute
				# multiply final value of using_energy by this amount of energy
				active_minutes = active_minutes + 1 

			history[i] = update_history(history[i], entry_array[i])
			if (edited):
				all_policy_actions.write(t + "\t" + str(entry_array[i]) + "\t" + str(timeInPolicy[i]) + "\t" + str(length_of_policy[i]) + "\t" + action + "\t" + cl + "***" + "\n")
			else:
				all_policy_actions.write(t + "\t" + str(entry_array[i]) + "\t" + str(timeInPolicy[i]) + "\t" + str(length_of_policy[i]) + "\t" + action + "\t" + cl + "\n")

		timer = timer + 1
		entry = datastream.readline()

	energy = calculate_energy(active_minutes)
	name = savename.split(".")
	fo = open(name[0]+"_summary.txt", "w")
	
	fo.write("ENERGY USAGE: " + str(energy) + "\n")
	fo.write("number of active minutes: " + str(active_minutes) +"\n")
	fo.write("number of occupancy events: " + str(total_events) + "\n")
	fo.write("number of wasted minutes: " + str(num_wasted_mins) + "\n")
	fo.write("number contracts renewed in middle: " + str(num_mid_renew) + "\n")
	fo.write("number contracts created from nothing: " + str(num_turn_on) + "\n")
	all_policy_actions.close()
	fo.close()



### generate all data files ###


hist_length = 10

filename = "experiment_data/first_week.txt"
savename = "hist10_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "hist10_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "hist10_third.txt"
runExperiment(filename, hist_length, savename)


hist_length = 20

filename = "experiment_data/first_week.txt"
savename = "hist20_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "hist20_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "hist20_third.txt"
runExperiment(filename, hist_length, savename)


hist_length = 30

filename = "experiment_data/first_week.txt"
savename = "hist30_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "hist30_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "hist30_third.txt"
runExperiment(filename, hist_length, savename)

hist_length = 40

filename = "experiment_data/first_week.txt"
savename = "hist40_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "hist40_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "hist40_third.txt"
runExperiment(filename, hist_length, savename)

hist_length = 60

filename = "experiment_data/first_week.txt"
savename = "hist60_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "hist60_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "hist60_third.txt"
runExperiment(filename, hist_length, savename)











