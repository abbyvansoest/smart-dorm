
# select policy for each time period based on current activity
def choosePolicy(cur_activity):

	if (cur_activity == 0):
		return 0
	
	elif (cur_activity == 1):
		return 1

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
def runExperiment(datafile, contract_length, savename):

	LEAVE_OFF = 0
	RENEW = 1

	datastream = open(datafile, "rw+")

	timer = 0
	num_mid_renew = 0
	num_turn_on = 0
	num_expired = 0

	all_policy_actions = open(savename, "w")

	#  read in first line - has number of sensors being used
	num_sensors = int(datastream.readline())
	print "number of sensors: " + str(num_sensors)
	
	timeInPolicy = [0] * num_sensors

	#  for each line in the file (represents a minute), read in sensor information
	#  select a policy for each sensor
	#  update sensor-specifically
	entry = datastream.readline()
	while (entry != ""):

		t = getTime(timer);

		if (entry == "\n"):
			break
		entry.replace("\n", "")
		entry_array = entry.split()
		#print entry_array

		# for each sensor
		for i in range(0,num_sensors):

			write_time_left = False

		#	print "i: " + str(i)
			if (len(entry_array) != num_sensors):
				print "ERROR"
				break

			#print entry_array[i]
			#  entry_array[i] = current activation status of sensor i
			#  policy = selected policy for sensor 
			#  time_left = time remaining in the contract for sensor i
			policy = choosePolicy(int(entry_array[i]))
			time_left = timeInPolicy[i]
			action = ""

			if (policy == RENEW):

				write_time_left = True

				#  check if turning on or renewing in the middle of a contract
				if (time_left > 0):
					num_mid_renew = num_mid_renew + 1
					action = "RENEWED"
				
				#  or if turning on for the first time (from black out)
				else:
					num_turn_on = num_turn_on + 1
					action = "TURNED ON"
				
				timeInPolicy[i] = contract_length
			
			elif (policy == LEAVE_OFF):
				# if  just expired
				if (time_left == 1):
					num_expired = num_expired + 1
					action = "CONTRACT EXPIRED"
				
				elif (time_left > 1):
					action = "LIVING OUT CONTRACT"
				
				else:
					action = "LEFT OFF"
	
				# decrement time left in i's contract if any time remains
				if (time_left > 0):
					timeInPolicy[i] = timeInPolicy[i] - 1

		# 	print t
		# 	print entry
		# 	print action
		# 	print "time left: " + str(timeInPolicy[i])

	 		all_policy_actions.write(str(timer) + "\t" + t + "\t" + str(time_left) + "\t" + action + "\n")

		# print "*************\n"
		timer = timer + 1
		entry = datastream.readline()

	print num_mid_renew
	print num_turn_on

	all_policy_actions.write("number contracts renewed in middle: " + str(num_mid_renew) + "\n")
	all_policy_actions.write("number contracts created from nothing: " + str(num_turn_on) + "\n")
	all_policy_actions.write("number contracts expired: " + str(num_expired) + "\n")
	all_policy_actions.close()

contract_length = 5

filename = "experiment_data/first_week.txt"
savename = "selected_policies_first5.txt"
runExperiment(filename, contract_length, savename)

filename = "experiment_data/second_week.txt"
savename = "selected_policies_second5.txt"
runExperiment(filename, contract_length, savename)

filename = "experiment_data/third_week.txt"
savename = "selected_policies_third5.txt"
runExperiment(filename, contract_length, savename)

contract_length = 10

filename = "experiment_data/first_week.txt"
savename = "selected_policies_first10.txt"
runExperiment(filename, contract_length, savename)

filename = "experiment_data/second_week.txt"
savename = "selected_policies_second10.txt"
runExperiment(filename, contract_length, savename)

filename = "experiment_data/third_week.txt"
savename = "selected_policies_third10.txt"
runExperiment(filename, contract_length, savename)

contract_length = 15

filename = "experiment_data/first_week.txt"
savename = "selected_policies_first15.txt"
runExperiment(filename, contract_length, savename)

filename = "experiment_data/second_week.txt"
savename = "selected_policies_second15.txt"
runExperiment(filename, contract_length, savename)

filename = "experiment_data/third_week.txt"
savename = "selected_policies_third15.txt"
runExperiment(filename, contract_length, savename)

contract_length = 20

filename = "experiment_data/first_week.txt"
savename = "selected_policies_first20.txt"
runExperiment(filename, contract_length, savename)

filename = "experiment_data/second_week.txt"
savename = "selected_policies_second20.txt"
runExperiment(filename, contract_length, savename)

filename = "experiment_data/third_week.txt"
savename = "selected_policies_third20.txt"
runExperiment(filename, contract_length, savename)

contract_length = 30

filename = "experiment_data/first_week.txt"
savename = "selected_policies_first30.txt"
runExperiment(filename, contract_length, savename)

filename = "experiment_data/second_week.txt"
savename = "selected_policies_second30.txt"
runExperiment(filename, contract_length, savename)

filename = "experiment_data/third_week.txt"
savename = "selected_policies_third30.txt"
runExperiment(filename, contract_length, savename)



