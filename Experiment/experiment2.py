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
	MID = 4

	zone = 1
	upper_threshold = .75
	lower_threshold = .1

	history_length = len(history)
	half_len = int(history_length/2)
	hist1 = history[0:half_len]
	hist2 = history[half_len:len(history)+1]

	freq = 0
	for item in history:
		thing = int(item)
		if thing == 1:
			freq = freq+ 1
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

	if (freq2 > freq1 + zone):
		return INCREASING
	elif (freq2 < freq1 - zone):
		return DECREASING
	else:
		ratio = float(freq) / float(history_length)
		if (ratio > upper_threshold):
			return HIGH_FREQ
		elif (ratio < lower_threshold):
			return LOW_FREQ
		else:
			return MID

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
	MID = 4

	LOW = 0
	HIGH = 15
	INCR = 1

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
			classification = classify(history[i])
			change = False
			if (prev_classify != classification):
				stored_classifications[i] = classification
				change = True
				num_changes = num_changes + 1
				all_policy_actions.write("CATEGORY CHANGE: " + str(prev_classify) + " to " + str(classification) + "\n")
				all_policy_actions.write(str(history[i]) + "\n")
			time_left = timeInPolicy[i]
			action = ""

			# use classification to decide settings
			if (classification == LOW_FREQ):
				# set policy to turn off immediately - no time left
				# if activated in this minute, turn on only for LOW minutes
				length_of_policy[i] = LOW

			if (classification == INCREASING):
				# increase time being added to policy renewal based on frequency/distribution data
				length_of_policy[i] = length_of_policy[i] + INCR

			if (classification == DECREASING):
				# decrease time being added to policy renewal based on frequency/distribution data
				length_of_policy[i] = length_of_policy[i] - INCR

			if (classification == HIGH_FREQ):
				# set policy to turn on for HIGH minutes whenever activated
				length_of_policy[i] = HIGH


			# handle current status update
			if (int(entry_array[i]) == 1):
				if (time_left >= 1):
					action = "CONTRACT RENEWED"
					num_mid_renew = num_mid_renew + 1
				elif (time_left == 0):
					action = "TURN ON"
					num_turn_on = num_turn_on + 1
				timeInPolicy[i] = length_of_policy[i]

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

			history[i] = update_history(history[i], entry_array[i])
			all_policy_actions.write(t + "\t" + str(entry_array[i]) + "\t" + str(timeInPolicy[i]) + "\t" + str(length_of_policy[i]) + "\t" + action + "\n")

		timer = timer + 1
		entry = datastream.readline()

	all_policy_actions.write("number contracts renewed in middle: " + str(num_mid_renew) + "\n")
	all_policy_actions.write("number contracts created from nothing: " + str(num_turn_on) + "\n")
	all_policy_actions.write("number contracts expired: " + str(num_expired) + "\n")
	all_policy_actions.write("number contracts left off: " + str(num_leave_off) + "\n")
	all_policy_actions.write("number of category changes made: " + str(num_changes) + "\n")
	all_policy_actions.close()


hist_length = 10

filename = "test_datafile1.txt"
savename = "policies_test_hist.txt"
runExperiment(filename, hist_length, savename)






