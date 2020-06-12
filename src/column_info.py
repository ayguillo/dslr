from math import sqrt

def		column_info(column):
	count, mean, min = len(column), 0, float('inf')
	for nb in column:
		# print(type(mean), "nb=",nb)
		try :
			mean += float(nb)
			if float(nb) < min:
				min = float(nb)
		except ValueError :
			mean = mean
			count -= 1
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

# info = column_info({1, 2, 3, 4})
# print("count: ", info[0])
# print("mean:  ", info[1])
# print("std:   ", info[2])
# print("min:   ", info[3])
# print("25%:   ", info[4])
# print("50%:   ", info[5])
# print("75%:   ", info[6])
# print("max:   ", info[7])