
# animation module for a "day in the life" of the occupancy sensors in Bloomberg Hall
# takes in data assocaited with 19 different sensors
# for each time step, shows what sensors are active

# display basement, first, second, third, and fourht floor maps
# array of Sensor objects, each with floor (image), pixel location, status
# at each timestep, read in data from each sensor 

# sensors we have:
# FIRST FLOOR
	# OS_bloom-hall131
	# OS_bloom-hall132
	# OS_corr122
	# OS_Corr130A
	# OS_Corr132
	# OS_Hall121

#SECOND FLOOR
	# OS_Corr257
	# OS_Corr260
	# OS_Corr264
	# OS_Corr266
	# OS_Corr272
	# OS_Rm253

# THIRD FLOOR
	# OS_Corr356
	# OS_Corr357
	# OS_Corr360
	# OS_Corr364
	# OS_Corr366
	# OS_Rm353

#############################################################################
from Tkinter import *
from PIL import Image, ImageTk
import sys


master1 = Toplevel()
master2 = Toplevel()
master3 = Toplevel()

floor1_im = Image.open('Bloomberg1.png')
floor2_im = Image.open('Bloomberg2.png')
floor3_im = Image.open('Bloomberg3.png')
w1, h1 = floor1_im.size
w2, h2 = floor2_im.size
w3, h3 = floor3_im.size

canvas1 = Canvas(master1, width=w1, height=h1)
canvas1.pack()
photo1 = ImageTk.PhotoImage(floor1_im)
canvas1.create_image(0,0, anchor=NW, image=photo1)

canvas2 = Canvas(master2, width=w2, height=h2)
canvas2.pack()
photo2 = ImageTk.PhotoImage(floor2_im)
canvas2.create_image(0,0, anchor=NW, image=photo2)

canvas3 = Canvas(master3, width=w3, height=h3)
canvas3.pack()
photo3 = ImageTk.PhotoImage(floor3_im)
canvas3.create_image(0,0, anchor=NW, image=photo3)

mainloop()

off = 0
on = 1

# initialize sensor objects
sensors_first_floor = []
sensors_second_floor = []
sensors_third_floor = []

#FIRST FLOOR
# OS_bloom-hall131
s1 = Sensor(440, 265, off, "data_filename.txt", 1)
sensors_first_floor.append(s1)
# OS_bloom-hall132
s2 = Sensor(500, 190, off, "data_filename.txt", 1)
sensors_first_floor.append(s2)
# OS_corr122
s3 = Sensor(472, 492, off, "data_filename.txt", 1)
sensors_first_floor.append(s3)
# OS_Corr130A
s4 = Sensor(445, 395, off, "data_filename.txt", 1)
sensors_first_floor.append(s4)
# OS_Corr132
s5 = Sensor(522, 260, off, "data_filename.txt", 1)
sensors_first_floor.append(s5)
# OS_Hall121
s6 = Sensor(360, 420, off, "data_filename.txt", 1)
sensors_first_floor.append(s6)

#SECOND FLOOR
# OS_Corr257
s7 = Sensor(240, 350, off, "data_filename.txt", 2)
sensors_second_floor.append(s7)
# OS_Corr260	
s8 = Sensor(250, 220, off, "data_filename.txt", 2)
sensors_second_floor.append(s8)
# OS_Corr264
s9 = Sensor(385, 370, off, "data_filename.txt", 2)
sensors_second_floor.append(s9)
# OS_Corr266
s10 = Sensor(530, 390, off, "data_filename.txt", 2)
sensors_second_floor.append(s10)
# OS_Corr272
s11 = Sensor(650, 410, off, "data_filename.txt", 2)
sensors_second_floor.append(s11)
# OS_Rm253
s12 = Sensor(130, 370, off, "data_filename.txt", 2)
sensors_second_floor.append(s12)


#THIRD FLOOR
# OS_Corr356
s13 = Sensor(220, 180, off, "data_filename.txt", 3)
sensors_third_floor.append(s13)
# OS_Corr357
s14 = Sensor(230, 365, off, "data_filename.txt", 3)
sensors_third_floor.append(s14)
# OS_Corr360
s15 = Sensor(245, 230, off, "data_filename.txt", 3)
sensors_third_floor.append(s15)
# OS_Corr364
s16 = Sensor(335, 385, off, "data_filename.txt", 3)
sensors_third_floor.append(s16)
# OS_Corr366
s17 = Sensor(505, 405, off, "data_filename.txt", 3)
sensors_third_floor.append(s17)
# OS_Rm353
s18 = Sensor(120, 405, off, "data_filename.txt", 3)
sensors_third_floor.append(s18)


prev_time = 0

# for each timestep, access next data field for each sensor.
# update status to on or off 
# update image 
while (dataAvailable()):

	# find closest time to prev time
	# get set of all nodes that have an entry at that time
	update_set, cur_time = find_updates(prev_time)
	
	# update their visualization on map
	for sensor in update_set:
		if (sensor.floor == 1):
			canvas = canvas1
		elif (sensor.floor == 2):
			canvas = canvas2
		elif (sensor.floor == 3):
			canvas = canvas3

		if (sensor.status == on):
			# draw red dot on image
			canvas.create_shape(sensor.x, sensor.y, color="red")
		elif (sensor.status == off):
			continue

	# update times
	prev_time = cur_time

# close things?	


# do all sensors have more available data?
def dataAvailable():

	for first in sensors_first_floor:
		if (first.is_empty):
			return false
	for second in sensors_second_floor:
		if (second.is_empty):
			return false
	for third in sensors_third_floor:
		if (third.is_empty):
			return false

	return true

# find the nearest time available in a dataset
def find_updates(time):

	min_t = 100000
	sensor_set = []

	for first in sensors_first_floor:
		if (first.heap[0] < time):
			print 'Error'
			return
		if (first.heap[0] < min_t):
			min_t = first.heap[0]
			sensor_set = []
			sensor_set.add(first)
		elif (first.heap[0] == min_t):
			sensor_set.add(first)

	for second in sensors_second_floor:
		if (second.heap[0] < time):
			print 'Error'
			return
		if (second.heap[0] < min_t)
			min_t = second.heap[0]
			sensor_set = []
			sensor_set.add(second)
		elif (second.heap[0] == min_t):
			sensor_set.add(second)

	for third in sensors_third_floor:
		if (third.heap[0] < time):
			print 'Error'
			return
		if (third.heap[0] < min_t)
			min_t = third.heap[0]
			sensor_set = []
			sensor_set.add(third)
		elif (third.heap[0] == min_t):
			sensor_set.add(third)

	# pop heap top for updated sensors
	for sen in sensor_set:
		sen.remove_next()

	return sensor_set, min_t


