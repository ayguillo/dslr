import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import pandas as pd
import os
import sys
from normalize import normalize_numpy
from reg_fit import regression

def get_notes(data):
	new_df = data[["Astronomy", "Ancient Runes"]].copy()
	new_df = normalize_numpy(new_df.to_numpy())
	# print(len(new_df))
	new_df = np.hstack((np.ones((len(new_df),1)), new_df))
	# print(new_df)
	return new_df

def get_houses(data):
	new_df = data["Hogwarts House"].replace(
		["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"],
		[1, 2, 3, 4])
	return new_df.to_numpy()[:,np.newaxis]

def compute(data):
	# a = get_notes(data)
	# print(get_houses(data))
	# print(np.zeros((3, 1)))
	x = regression(get_notes(data), get_houses(data), np.zeros((3, 1)), 0.1, 100)
	print(x.gradient_descent())
	print(x.theta)
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="define your file", type = str)
	args = parser.parse_args()
	if not os.path.exists(args.file) or not os.path.isfile(args.file):
		print("File error:", args.file)
		sys.exit()
	data = pd.read_csv(args.file)
	if "Hogwarts House" not in data.columns or "Ancient Runes" not in data.columns or "Astronomy" not in data.columns:
		print('Need columns: "Hogwarts House", "Ancient Runes", "Astronomy"')
	else:
		compute(data)