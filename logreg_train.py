import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import pandas as pd
import os
import sys

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def compute_cost(X, y, theta):
    m = len(y)
    h = sigmoid(X @ theta)
    epsilon = 1e-5
    cost = (1/m)*(((-y).T @ np.log(h + epsilon))-((1-y).T @ np.log(1-h + epsilon)))
    return cost

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="define your file", type = str)
	args = parser.parse_args()
	if not os.path.exists(args.file) or not os.path.isfile(args.file):
		print("File error:", args.file)
		sys.exit()
	data = pd.read_csv(args.file)