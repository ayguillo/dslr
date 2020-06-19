#!/usr/bin/python3

import numpy as np
import argparse
import pandas as pd
import os
import sys
from src.normalize import normalize_numpy

def predict_this_stud(notes, thetas):
	house = 0
	best = thetas[0][0] + notes[0] * thetas[0, 1] + notes[1] * thetas[0, 2] + notes[2] * thetas[0, 3]
	# res = "G: " + str(best) + " | "
	# print(notes[0])
	# sys.exit()
	for i in range (1, 4):
		tmp = thetas[i, 0] + notes[0] * thetas[i, 1] + notes[1] * thetas[i, 2] + notes[2] * thetas[i, 3]
		# res += " | " + str(i) + ": " + str(tmp)
		if tmp > best:
			best = tmp
			house = i
	# return (res)
	if house == 0:
		return "Gryffindor"
	if house == 1:
		return "Slytherin"
	if house == 2:
		return "Ravenclaw"
	if house == 3:
		return "Hufflepuff"

def compute(data):
	notes = normalize_numpy(data[["Astronomy", "Ancient Runes", "Herbology"]].copy().to_numpy())
	if len(notes) < 1:
		print("Not enough data")
		return
	notes[np.isnan(notes)] = 0.5
	thetas = pd.read_csv(".save_model.csv", delimiter=',').to_numpy()
	res = "Index,Hogwarts House"
	for i in range(len(notes)):
		res += "\n" + str(i) + "," + predict_this_stud(notes[i], thetas)
	f = open("houses.csv", "w")
	f.write(res)
	f.close()
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="define your file", type = str)
	args = parser.parse_args()
	if not os.path.exists(args.file) or not os.path.isfile(args.file):
		print("File error:", args.file)
		sys.exit()
	if not os.path.exists(".save_model.csv") or not os.path.isfile(".save_model.csv"):
		print("File error: no '.save_model.csv' found")
		sys.exit()
	try:
		data = pd.read_csv(args.file)
	except pd.errors.EmptyDataError:
		print("Empty file")
		sys.exit(-1)
	if "Ancient Runes" not in data.columns or "Astronomy" not in data.columns or "Herbology" not in data.columns:
		print('Need columns: "Ancient Runes", "Astronomy", "Herbology"')
	else:
		try:
			compute(data)
		except:
			print("Compute error")