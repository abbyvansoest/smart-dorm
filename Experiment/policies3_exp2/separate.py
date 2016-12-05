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

	# remove final 6 (worded) entries 
	length = len(mylist)
	mylist = mylist[:length - 6]
	length = len(mylist)

	name = "separated/"+f
	end_file = open(name, "w")

	#  go through list of strings starting at
	print length
	increment = 6
	for start in range(0, 6):
		index = start
		while (index < length):
			end_file.write(mylist[index])
			index = index + increment
		end_file.write("*********************\n")

	end_file.close()





