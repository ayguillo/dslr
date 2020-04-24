# count, mean, std, min, max, percentage

import sys

def		column_info(column):
	count, mean, min = len(column), 0, float('inf')
	for nb in column:
		mean += nb
		if nb < min:
			min = nb
	mean /= count
	std, max = 0, float('-inf')
	for nb in column:
		std += abs(mean - nb)
		if nb > max:
			max = nb
	std /= count
	return (count, mean, std, min, (min + mean) / 2, mean, (mean + max) / 2, max)

# info = column_info({1, 2, 3, 4})
# print("count: ", info[0])
# print("mean:  ", info[1])
# print("std:   ", info[2])
# print("min:   ", info[3])
# print("25%:   ", info[4])
# print("50%:   ", info[5])
# print("75%:   ", info[6])
# print("max:   ", info[7])