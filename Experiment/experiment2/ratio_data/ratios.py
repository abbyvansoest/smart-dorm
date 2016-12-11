import matplotlib.pyplot as plt
import numpy as np

def autolabel(rects):
    # attach some text labels
    firstRect = True;
    for rect in rects:
        height = rect.get_height()
        if (firstRect):
        	ax.text(rect.get_x() + (rect.get_width()+.5)/2., 1.01*height + 250,
    	            '%d' % int(height*2),
        	        ha='center', va='bottom', rotation='vertical')
        	firstRect = False;
        else:
	        ax.text(rect.get_x() + (rect.get_width()+.01)/2., 1.01*height + 250,
    	            '%d' % int(height),
        	        ha='center', va='bottom', rotation='vertical')

length = 30
filename = "ratios" + str(length) + ".txt"
ratio_file = open(filename, "rw+")

entry = ratio_file.readline()
freq_count = [0] * (length+1)
while (entry != ""):
	# convert to decimal
	# add to histogram list
	decimal = float(entry)
	index =  int(round(decimal * length))
	freq_count[index] = freq_count[index] + 1
	entry = ratio_file.readline()

# chart histogram
fig = plt.figure()
ax = fig.add_subplot(111)
width = .5
ind = []
for i in range(length+1):
	ind.append(float(i))
print ind
print freq_count
rects1 = ax.bar(ind, freq_count, width, color='black')

autolabel(rects1)
x1,x2,y1,y2 = plt.axis()
plt.axis((x1,x2+1,y1,y2+750))
ax.set_xlabel('Number of active sensors in history')
ax.set_ylabel('Frequency')
ax.set_title('Frequency of activity, history length = ' + str(length))

plt.show()