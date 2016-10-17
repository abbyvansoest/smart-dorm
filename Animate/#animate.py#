
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

	# need to establish (x,y) locations of these sensors on the images

#############################################################################
from PIL import Image, ImageDraw
import sys

floor1 = Image.open('Bloomberg1.jpg')
floor2 = Image.open('Bloomberg2.jpg')
floor3 = Image.open('Bloomberg3.jpg')

off = 0
on = 1

# initialize sensor objects
sensors_first_floor = []
sensors_second_floor = []
sensors_third_floor = []

#FIRST FLOOR
# OS_bloom-hall131
s1 = Sensor(x, y, off, "data_filename.txt")
sensors_first_floor.append(s1)
# OS_bloom-hall132
s2 = Sensor(x, y, off, "data_filename.txt")
sensors_first_floor.append(s2)
# OS_corr122
s3 = Sensor(x, y, off, "data_filename.txt")
sensors_first_floor.append(s3)
# OS_Corr130A
s4 = Sensor(x, y, off, "data_filename.txt")
sensors_first_floor.append(s4)
# OS_Corr132
s5 = Sensor(x, y, off, "data_filename.txt")
sensors_first_floor.append(s5)
# OS_Hall121
s6 = Sensor(x, y, off, "data_filename.txt")
sensors_first_floor.append(s6)

#SECOND FLOOR
# OS_Corr257
s7 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s7)
# OS_Corr260	
s8 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s8)
# OS_Corr264
s9 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s9)
# OS_Corr266
s10 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s10)
# OS_Corr272
s11 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s11)
# OS_Rm253
s12 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s12)


#THIRD FLOOR
# OS_Corr356
s13 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s13)
# OS_Corr357
s14 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s14)
# OS_Corr360
s15 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s15)
# OS_Corr364
s16 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s16)
# OS_Corr366
s17 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s17)
# OS_Rm353
s18 = Sensor(x, y, off, "data_filename.txt")
sensors_second_floor.append(s18)

###
draw = ImageDraw.Draw(im)
draw.line((0, 0) + im.size, fill=128)
draw.line((0, im.size[1], im.size[0], 0), fill=128)
del draw

# write to stdout
im.save('draw.jpg')






