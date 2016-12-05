def get_hour(timer):
	hour = int(timer / 60)
	hour = int(hour % 24)
	return hour

# read in all data from all sensors from all floors over the week
files = ["experiment_data/first_week.txt", "experiment_data/second_week.txt", "experiment_data/third_week.txt"]

frequencies = [0] * 24
total_num_counted = [0] * 24

for f in files:

	fo = open(f, "rw+")
	timer = 0
	entry = fo.readline()

	while (entry != ""):
		hour = get_hour(timer)
		entry_array = entry.split()
		for e in entry_array:
			frequencies[hour] = frequencies[hour] + int(e)
		total_num_counted[hour] = total_num_counted[hour] + len(entry_array)
		entry = fo.readline()

		timer = timer + 1 

ratios = [float(freq) / float(7560) for freq in frequencies]
print ratios
