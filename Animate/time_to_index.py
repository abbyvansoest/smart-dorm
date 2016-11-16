#def time_to_index(time):
	# split at space character into (date) and (time)
array = [0] * 1440
print len(array)

time = '12/12/12 23:59'
t = time.split(" ")
date = t[0]
time = t[1]
hm = time.split(":")
hour = int(hm[0])
mins = int(hm[1])

index =  hour*60 + mins
print index
array[index] = array[index] + 1
print array
#return index