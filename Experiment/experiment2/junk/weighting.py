import math 

#sequence = [1,1,1,1,0,0,1,1,0,0,0,0,1,1,1]
sequence = [0,0,0,0,0,0,1,1,0,0,0,1,1,1,1]
sequence = [1,0,1,0,1,1,1,0,1,0,1,0,1,1,1]
sequence = [0,0,0,0,0,0,1,1,1,1,0,1,1,1,1]

dcg_ones = 0.0
dcg_back = 0.0
dcg_zeros = 0.0
dcg_zeros_back = 0.0

one_freq = 0
zero_freq = 0


for j in range(1,16):
	i = 16 - j
	
	dcg_ones = dcg_ones + sequence[i-1]/float(j*j)
	dcg_back = dcg_back + sequence[j-1]/float(j*j)

	if (sequence[i-1] == 0):
		use1 = 1
	else:
		use1 = 0
	if (sequence[j-1] == 0):
		use2 = 1
	else:
		use2 = 0
	dcg_zeros = dcg_zeros + use1/float(j*j)
	dcg_zeros_back = dcg_zeros_back + use2/float(j*j)

	if (sequence[j-1]==1):
		one_freq = one_freq + 1
	else:
		zero_freq = zero_freq + 1

print dcg_ones
print dcg_back
print dcg_zeros
print "\n"
print dcg_ones/one_freq
print dcg_back/one_freq
print dcg_ones/one_freq - dcg_back/one_freq
print "\n"
print dcg_zeros/zero_freq
print dcg_zeros_back/zero_freq
print dcg_zeros/zero_freq - dcg_zeros_back/zero_freq  

# if diff is negative, weight is stronger on the earlier part
# if positive stronger on later part
# # if similar both ways, symmterical
# 	thresh = .075
# 	if (mag < thresh):
# 		return STEADY
