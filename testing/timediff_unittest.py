cur_time = "10/2/16 12:02"
prev_time = "10/1/16 11:59"

print("current time is " + cur_time)
print("prev time is " + prev_time)

diff = -1
# split at space character into (date) and (time)
t1 = prev_time.split(" ")
date1 = t1[0]
time1 = t1[1]
hm1 = time1.split(":")
hour1 = int(hm1[0])
min1 = int(hm1[1])

t2 = cur_time.split(" ")
date2 = t2[0]
time2 = t2[1]
hm2 = time2.split(":")
hour2 = int(hm2[0])
min2 = int(hm2[1])

h_diff = hour2 - hour1
m_diff = min2 - min1
if (h_diff == 0):
	diff = m_diff
elif (m_diff < 0):
	diff = (60 + m_diff)
else:
	diff = (h_diff*60 + m_diff)

# sanity checks
if (hour2 < hour1):
	print("WRONG")
if ((hour2 == hour1) and (min2 < min1)):
	print("WRONG")

print ("diff is " + str(diff))

