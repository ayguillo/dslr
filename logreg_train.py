import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import pandas as pd
import os
import sys
from normalize import normalize_numpy
from reg_fit import regression


def save_theta(theta0, theta1, theta2):
	with open(".save_model.csv", 'w', newline='') as csvfile:
  	  spamwriter = csv.writer(csvfile, delimiter=',')
  	  spamwriter.writerow(["Theta0", "Theta1", "Theta2"])
  	  spamwriter.writerow([theta0, theta1, theta2])

def get_notes_houses(data):
	new_df = data[["Hogwarts House", "Astronomy", "Ancient Runes"]].copy().dropna()
	notes = normalize_numpy(new_df[["Astronomy", "Ancient Runes"]].copy().to_numpy())
	# print(notes)
	notes = np.hstack((np.ones((len(notes),1)), notes))
	houses = data["Hogwarts House"].replace(
		["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"],
		[1, 2, 3, 4])
	houses = houses.to_numpy()[:,np.newaxis]
	print(notes)
	# print(houses)
	return (notes, houses)

def get_houses(data):
	new_df = data["Hogwarts House"].replace(
		["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"],
		[1, 2, 3, 4])
	return new_df.to_numpy()[:,np.newaxis]

def single_house_regression(notes, houses, house_number):
	binary_houses = np.where(houses!=house_number, 0, houses)
	binary_houses = np.where(binary_houses==house_number, 1, binary_houses)
	# print(binary_houses)
	x = regression(notes, binary_houses, np.zeros((3, 1)), 0.1, 100)
	# print(x.gradient_descent())
	# print(x.theta.T.tolist())
	return(x.theta.T)

# def clean_nan(notes, houses):

def compute(data):
	notes, houses = get_notes_houses(data)
	# houses = get_houses(data)
	# notes, houses = clean_nan(notes, houses)
	# houses_theta = []
	# print(np.zeros((3, 1)))
	# for i in range (1, 5):
	single_house_regression(notes, houses, 2)
	# print(houses_theta)
	# x = regression(get_notes(data), get_houses(data), np.zeros((3, 1)), 0.1, 100)
	# print(x.gradient_descent())
	# print("\nthetas:\n", x.theta)
	

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