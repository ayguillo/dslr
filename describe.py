#!/usr/bin/python3

import csv
from src.column_info import column_info
import os
import pandas as pd
import argparse
import sys

def args_is_r(df, args, all=True):
	row = []
	arg = args.row.split(',')
	for r in arg :
		row.append(r.strip())

	if (all == True):
		try :
			line = 0
			del_line = []
			for i, n in df.iterrows():
				if (i not in row):
					del_line.append(i)
				line += 1
			df = df.drop(del_line)
			return(df)
		except KeyError as e:
			print("Check argument please : {} not found".format(e))
			return(df)
	else :
		try :
			df = df[row]
			return(df)
		except KeyError as e:
			print("Check argument please : {} not found".format(e))
			return(df)

def is_number(str):
	try:
		float(str)
	except ValueError:
		return False
	else:
		return isinstance(float(str), (int,float))

def describe(data, args):
	rows, columns = os.popen('stty size', 'r').read().split()
	tab_feature, tab_res, count_line, n_feature = [], [], 0, 0
	index = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
	len_i = len(index)
	if len(data) < 1 or len(data[0]) < 2:
		print("Not enough data")
		return None
	for line in data :
		if (is_number(line[1])):
			tab_res.append(column_info(data[count_line][1:]))
			tab_feature.append(line[0])
			n_feature += 1
		count_line += 1
	if (args.all):
		df = pd.DataFrame(tab_res, columns = index, index = tab_feature)
		if (args.row):
			df = args_is_r(df, args)
	else :
		df = pd.DataFrame(tab_res, columns = index, index = tab_feature).T
		if (args.row):
			df = args_is_r(df, args, all=False)
	if (args.save):
		df.to_csv(args.save, index = True, header=True)
	print(df)

def get_dataset(file):
	f = open(file, "r")
	csv_reader = csv.reader(f, delimiter=',')
	count_line = 0
	dataset = []
	for line in csv_reader:
		if (count_line == 0):
			len_data  = len(line)
			for j in range (0, len_data):
				dataset.append([])
		if (len(line) != len_data):
			f.close()
			print("File not well formed")
			return
		count_row = 0
		for row in line :
			dataset[count_row] += {row}
			count_row += 1
		count_line += 1
	f.close()
	return (dataset)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="define your file", type = str)
	parser.add_argument("-a","--all", help="print all data", action="store_true")
	parser.add_argument("-s","--save", help="Save result in csv", type = str)
	parser.add_argument("-r","--row", help="Choose row to print", type = str)
	args = parser.parse_args()
	if not os.path.exists(args.file) or not os.path.isfile(args.file):
		print("File error:", args.file)
		sys.exit()
	data = get_dataset(args.file)
	describe(data, args)
