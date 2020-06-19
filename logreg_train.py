#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import csv
import os
import sys
from src.normalize import normalize_numpy
from src.reg_fit import regression

def plot_graph_cost(plot):
	max_iter = 0
	for i in range(len(plot)):
		if (len(plot[i]) > max_iter):
			max_iter = len(plot[i])
	for i in range(len(plot)):
		while (len(plot[i]) < max_iter):
			plot[i].append(plot[i][-1])
		if i == 0:
			color = 'r'
		if i == 1:
			color = 'g'
		if i == 2:
			color = 'b'
		if i == 3:
			color = 'y'
		plt.plot(range(max_iter), plot[i], color=color)
	plt.legend(['Gryffindor', 'Slytherin', 'Ravenclaw', 'Hufflepuff'])
	plt.title("Cost function")
	plt.show()

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

def single_house_regression(notes, houses, house_number, visualise):
	binary_houses = np.where(houses!=house_number, 0, houses)
	binary_houses = np.where(binary_houses==house_number, 1, binary_houses)
	x = regression(notes, binary_houses, np.zeros((4, 1)), 5, 7000)
	cost_history = x.gradient_descent()
	return(x.theta.T.tolist(), cost_history)

def compute(data, visualise):
	notes, houses = get_notes_houses(data)
	houses_theta, plot = [], []
	for i in range (1, 5):
		tmp_theta, tmp_cost = single_house_regression(notes, houses, i, visualise)
		houses_theta += tmp_theta
		plot.append(tmp_cost)
	save_theta(houses_theta)
	if visualise == True:
		plot_graph_cost(plot)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="define your file", type = str)
	parser.add_argument("-v","--visualise",help="define create files cost.png that represent the cost training result", action="store_true")
	args = parser.parse_args()
	if not os.path.exists(args.file) or not os.path.isfile(args.file):
		print("File error:", args.file)
		sys.exit()
	try:
		data = pd.read_csv(args.file)
	except pd.errors.EmptyDataError:
		print("Empty file")
		sys.exit(-1)
	if "Hogwarts House" not in data.columns or "Ancient Runes" not in data.columns or "Astronomy" not in data.columns or "Herbology" not in data.columns:
		print('Need columns: "Hogwarts House", "Ancient Runes", "Astronomy", "Herbology"')
	else:
		compute(data, args.visualise)