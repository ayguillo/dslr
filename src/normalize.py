import numpy as np
import sys
import csv
import pandas as pd

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
	min, max, length = min_max_length(column)
	max -= min
	if max == 0:
		print("Values error")
		sys.exit(-1)
	for i in range(length):
		try:
			column[i] = (column[i] - min) / max
		except TypeError:
			column[i] = column[i]

def		normalize_numpy(dataset):
	dataset = np.transpose(dataset)
	for i in range (len(dataset)):
		normalize_column(dataset[i])
	dataset = np.transpose(dataset)
	return (dataset)
