from math import sqrt
import sys

def		column_info(column):
	count, mean, min = len(column), 0, float('inf')
	for nb in column:
		try :
			mean += float(nb)
			if float(nb) < min:
				min = float(nb)
		except ValueError :
			mean = mean
			count -= 1
	if count < 2:
		print("Not enough data")
		sys.exit(-1)
	mean /= float(count)
	std, max = 0, float('-inf')
	for nb in column:
		try :
			std += (float(nb) - float(mean))**2
			if float(nb) > max:
				max = float(nb)
		except ValueError:
			max, std = max, std
	std = sqrt(std / (count - 1))
	return ([count, mean, std, min, (min + mean) / 2, mean, (mean + max) / 2, max])