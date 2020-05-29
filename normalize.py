import numpy as np
import sys
import csv
import pandas as pd
# from matrice_tools import transposition

def		min_max_length(column):
	min, max, length = sys.maxsize, -sys.maxsize, len(column)
	for i in range (length):
		try:
			if column[i] < min:
				min = column[i]
			if column[i] > max:
				max = column[i]
		except TypeError:
			min, max = min, max
	return min, max, length

def		normalize_column(column):
	# print(len(column))
	min, max, length = min_max_length(column)
	max -= min
	for i in range(length):
		try:
			column[i] = (column[i] - min) / max
		except TypeError:
			column[i] = column[i]

def		normalize_numpy(dataset):
	# print(dataset)
	dataset = np.transpose(dataset)
	# print(dataset)
	# print(len(dataset))
	for i in range (len(dataset)):
		normalize_column(dataset[i])
	# print(dataset)
	dataset = np.transpose(dataset)
	# print(dataset)
	return (dataset)


# if __name__ == "__main__":
# 	f = open(sys.argv[1], "r")
# 	csv_reader = csv.reader(f, delimiter=',')
# 	dataset = pd.read_csv(f, delimiter=',')
# 	normalize(dataset.to_numpy())