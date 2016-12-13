import glob

files = glob.glob("*.txt")
for fi in glob.glob('*summary*'):
	files.remove(fi)

for f in files: 

	fo = open(f, "rw+")
	#  read all lines into a list of strings
	mylist = []
	entry = fo.readline()
	while (entry != ""):
		mylist.append(entry)
		entry = fo.readline()

	name = "separated_"+f
	end_file = open(name, "w")

	#  go through list of strings starting at
	length = len(mylist)
	print length
	increment = 6
	for start in range(0, 6):
		index = start
		while (index < length):
			end_file.write(mylist[index])
			index = index + increment
		end_file.write("*********************\n")

	end_file.close()





