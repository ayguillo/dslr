import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import pandas as pd
import csv
import os
import sys
from normalize import normalize_numpy
from reg_fit import regression


def save_theta(thetas):
	with open(".save_model.csv", 'w', newline='') as csvfile:
  		spamwriter = csv.writer(csvfile, delimiter=',')
  		spamwriter.writerow(["Theta0", "Theta1", "Theta2", "Theta3"])
  		spamwriter.writerow(thetas[0])
  		spamwriter.writerow(thetas[1])
  		spamwriter.writerow(thetas[2])
  		spamwriter.writerow(thetas[3])

def get_notes_houses(data):
	new_df = data[["Hogwarts House", "Astronomy", "Ancient Runes", "Herbology"]].copy().dropna()
	notes = normalize_numpy(new_df[["Astronomy", "Ancient Runes", "Herbology"]].copy().to_numpy())
	notes = np.hstack((np.ones((len(notes), 1)), notes))
	houses = new_df["Hogwarts House"].replace(
		["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"],
		[1, 2, 3, 4])
	houses = houses.to_numpy()[:,np.newaxis]
	return (notes, houses)

def single_house_regression(notes, houses, house_number):
	binary_houses = np.where(houses!=house_number, 0, houses)
	binary_houses = np.where(binary_houses==house_number, 1, binary_houses)
	# print(binary_houses)
	# return ("hello")
	x = regression(notes, binary_houses, np.zeros((4, 1)), 5, 7000)
	x.gradient_descent()
	# print(x.theta)
	return(x.theta.T.tolist())

def compute(data):
	notes, houses = get_notes_houses(data)
	houses_theta = []
	# for small test, uncomment the 3 next lines <---------------------------------------------------------------------TESTS HERE
	# houses_theta = [[0], [0], [0], single_house_regression(notes, houses, 2)]
	# save_theta(houses_theta)
	# return

	print(notes)
	for i in range (1, 5):
		houses_theta += single_house_regression(notes, houses, i)
	save_theta(houses_theta)
	

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