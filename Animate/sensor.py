class OccSensor:

	def __init__(self, x, y, status, t, filename):
		self.x = x
		self.y = y
		self.status = status
		self.file = filename

	def update_time(t):
		self.time = t

	# load all data from file to be stored in Sensor structure
	def load_data():
