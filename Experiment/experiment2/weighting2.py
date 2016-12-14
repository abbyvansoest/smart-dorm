import math 
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import pylab
from scipy.stats import norm

def get_dcg(sequence):
	dcg_ones = 0.0
	dcg_back = 0.0
	dcg_zeros = 0.0
	dcg_zeros_back = 0.0

	one_freq = 0
	zero_freq = 0

	for j in range(1,len(sequence)+1):
		i = len(sequence)+1 - j
		
		dcg_ones = dcg_ones + sequence[i-1]/math.log(j+1,2)#float(j)
		dcg_back = dcg_back + sequence[j-1]/math.log(j+1,2)#float(j)

		if (sequence[i-1] == 0):
			use1 = 1
		else:
			use1 = 0
		if (sequence[j-1] == 0):
			use2 = 1
		else:
			use2 = 0
		dcg_zeros = dcg_zeros + use1/math.log(j+1,2)#float(j)
		dcg_zeros_back = dcg_zeros_back + use2/math.log(j+1,2)#float(j)

		if (sequence[j-1]==1):
			one_freq = one_freq + 1
		else:
			zero_freq = zero_freq + 1

	print dcg_ones
	print dcg_back
	print dcg_zeros
	print dcg_zeros_back
	print "\n"

	# print dcg_ones/one_freq
	# print dcg_back/one_freq
	if (one_freq == 0):
		diff1 = 0
	else:
		diff1 = dcg_ones/one_freq - dcg_back/one_freq
	print diff1
	

	# print dcg_zeros/zero_freq
	# print dcg_zeros_back/zero_freq
	if (zero_freq == 0):
		diff0 = 0
	else:
		diff0 = dcg_zeros/zero_freq - dcg_zeros_back/zero_freq 
	print diff0
	print "\n"

	return diff1, diff0


testing = 10

avgs = []

tester = [1,0,0,1,0,0,0,0,0,0]
# for i in range(testing):
# 	rand = random.random()
# 	add = 0
# 	if (rand < .3):
# 		add = 1
# 	tester.append(add)
dcg1, dcg0 = get_dcg(tester)

dcg1pos = math.fabs(dcg1)
dcg0pos = math.fabs(dcg0)

#	perc_change = (dcg1pos - dcg0pos)/((dcg0pos+dcg1pos)/2.0)
avg = (dcg1 + dcg0)/2.0
print "avg "+str(avg)
avgs.append(avg)

# fig, ax = plt.subplots(1)
# bin_boundaries = np.linspace(-1,1,150)

# weights = np.ones_like(avgs)/float(len(avgs))
# n, bins, rectangles = plt.hist(avgs, weights=weights, bins=bin_boundaries)
# # print n

# plt.axis([-.5, .5, 0, .4])  
# plt.title("PDF of the Normalized Average DCG of 0 and 1\n history length = 20\t number of trials = 10^6")
# plt.xlabel("Binned Average DCG")
# plt.ylabel("Probability of Occurance")

# sigma = np.std(avgs)
# mu = np.mean(avgs)
# textstr = "mean = "+str(round(mu,4)) + "\n" +"stddev = "+str(round(sigma,4))
# #plt.text(.78,.87, textstr, fontsize=12, transform=ax.transAxes)
# print "testing: " + str(testing)
# print sigma
# print mu

# x = np.linspace(-1,1,150)
# print x
# y = norm.pdf(x, mu, sigma)
# print y
# plt.plot(x, y, 'r--')
#plt.show()






