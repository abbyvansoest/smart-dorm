#  classify history in one of four categories and have set response based on that
	# increasing freq  -- increase the number of minutes you're keeping lights on for
	# decreasing freq  -- decrease the number of minutes you're keeping lights on for
	# steady high freq  --  keep on for X minutes
	# steady low freq  -- turn off/on immediately as activation sensed 



def classify(history):

	# classify history of length history_length based on criteria
	LOW_FREQ = 0
	INCREASING = 1 
	DECREASING = 2
	HIGH_FREQ = 3
	MID_FREQ = 4

	N = 5
	increment = float(1)/float(N)
	upper_threshold = .75
	lower_threshold = .1

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

	# compare the zones that the first and second halfs of the history were placed in
	# if in the same zone, maintain current activation policy
	# if X zones up/down, increase/decrease by X minutes
	compare = zone2 - zone1
	if (compare == 0):
		return MID_FREQ, 0
	if (compare < 0):
		return DECREASING, abs(compare)
	if (compare > 0):
		return INCREASING, compare

	return -1

def update_history(hist, next):
	history = hist
	history.append(next)
	del history[0]
	return history

def getTime(timer):
	hour = int(timer / 60)
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

	LOW = 0
	HIGH = 30
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

	all_policy_actions = open(savename, "w")

	#  read in first line - has number of sensors being used
	num_sensors = int(datastream.readline())	
	timeInPolicy = [LOW] * num_sensors

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

	using_energy = 0
	stored_classifications = [-1] * num_sensors
	length_of_policy = [LOW] * num_sensors
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
			classification, diff = classify(history[i])
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
				if (length_of_policy[i] + diff < HIGH):
					length_of_policy[i] = length_of_policy[i] + diff
				else:
					length_of_policy[i] = HIGH
				cl = "INCREASING"

			if (classification == DECREASING):
				# decrease time being added to policy renewal based on frequency/distribution data
				if (length_of_policy[i] - diff > 0):
					length_of_policy[i] = length_of_policy[i] - diff
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
				if (time_left >= 1):
					action = "CONTRACT RENEWED"
					num_mid_renew = num_mid_renew + 1
				elif (time_left == 0):
					action = "TURN ON"
					num_turn_on = num_turn_on + 1
				if (length_of_policy[i] > timeInPolicy[i]):
					timeInPolicy[i] = length_of_policy[i]
				elif (timeInPolicy[i] > 0):
					timeInPolicy[i] = timeInPolicy[i] - 1

			elif (int(entry_array[i]) == 0):
				if (time_left == 1):
					action = "LET EXPIRE"
					num_expired = num_expired + 1
				elif (time_left > 0):
					action = "WAIT LIFESPAN"
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
				using_energy = using_energy + 1 

			history[i] = update_history(history[i], entry_array[i])
			all_policy_actions.write(t + "\t" + str(entry_array[i]) + "\t" + str(timeInPolicy[i]) + "\t" + str(length_of_policy[i]) + "\t" + action + "\t" + cl + "\n")

		timer = timer + 1
		entry = datastream.readline()

	energy = using_energy * ENG_CONSUMED_PER_MIN
	print history_length
	print energy
	all_policy_actions.write("ENERGY USAGE: " + str(energy) + "\t" + str(using_energy) +"\n")
	all_policy_actions.write("number contracts renewed in middle: " + str(num_mid_renew) + "\n")
	all_policy_actions.write("number contracts created from nothing: " + str(num_turn_on) + "\n")
	all_policy_actions.write("number contracts expired: " + str(num_expired) + "\n")
	all_policy_actions.write("number contracts left off: " + str(num_leave_off) + "\n")
	all_policy_actions.write("number of category changes made: " + str(num_changes) + "\n")
	all_policy_actions.close()


### generate all test files ###

hist_length = 10

filename = "experiment_data/first_week.txt"
savename = "copy_policies_exp2/policies_hist10_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "copy_policies_exp2/policies_hist10_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "copy_policies_exp2/policies_hist10_third.txt"
runExperiment(filename, hist_length, savename)


hist_length = 20

filename = "experiment_data/first_week.txt"
savename = "copy_policies_exp2/policies_hist20_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "copy_policies_exp2/policies_hist20_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "copy_policies_exp2/policies_hist20_third.txt"
runExperiment(filename, hist_length, savename)



hist_length = 30

filename = "experiment_data/first_week.txt"
savename = "copy_policies_exp2/policies_hist30_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "copy_policies_exp2/policies_hist30_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "copy_policies_exp2/policies_hist30_third.txt"
runExperiment(filename, hist_length, savename)

hist_length = 40

filename = "experiment_data/first_week.txt"
savename = "copy_policies_exp2/policies_hist40_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "copy_policies_exp2/policies_hist40_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "copy_policies_exp2/policies_hist40_third.txt"
runExperiment(filename, hist_length, savename)

hist_length = 60

filename = "experiment_data/first_week.txt"
savename = "copy_policies_exp2/policies_hist60_first.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/second_week.txt"
savename = "copy_policies_exp2/policies_hist60_second.txt"
runExperiment(filename, hist_length, savename)

filename = "experiment_data/third_week.txt"
savename = "copy_policies_exp2/policies_hist60_third.txt"
runExperiment(filename, hist_length, savename)











