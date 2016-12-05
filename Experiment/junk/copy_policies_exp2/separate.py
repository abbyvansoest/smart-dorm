
filename = "policies_hist10_first.txt"
fo = open(filename, "rw+")

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

end_file = open("by_sensor.txt", "w")

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





