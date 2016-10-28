from heapq import heappush, heappop

class Sensor:

	def __init__(self, x, y, status, filename, floor):
		self.x = x
		self.y = y
		self.status = status
		self.file = filename
		self.floor = floor
		self.num, self.heap = load_data(filename)
		if (self.num == 0):
			self.is_empty = true
		else:
			self.is_empty = false

	# load all data from file to be stored in Sensor structure
	def load_data(filename):

		num_data_points = 0
		makeheap = []

		# read all lines
		line = filename.readline()

		while (line != ""):

			# create node tuple
			node = parse_line(line)
			# add to heap (should sort by 'quant' entry)
			heappush(makeheap, node)
			num_data_points = num_data_points + 1

			# read next line
			line = filename.readline()

		return num_data_points, makeheap


	# given a line from the data, parse into a tuple
	def parse_line(line):

		values = line.split("\t")
		day_time = values[0].split(" ")
		hour_min = day_time[1].split(":")
		hours = hour_min[0]
		minutes = hour_min[1]
		status = int(values[1])

		# quantification of time
		quant = 60*hours + minutes

		node = (quant, hours, minutes, status)
		return node

	# remove and return next most recent item
	def remove_next():
		node = heappop(self.heap)
		self.num = self.num - 1
		if (self.num == 0):
			self.is_empty = true
		return node




