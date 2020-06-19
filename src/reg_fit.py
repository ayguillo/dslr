import numpy as np
import time
import sys

class regression:

	def __init__(self, X, y, theta, learning_rate, iterations):
		self.X = X
		self.y = y
		self.theta = theta
		self.learning_rate = learning_rate
		self.iterations = iterations

	def sigmoid(self, z):
		return (1 / (1 + np.exp(-z)))

	def cost(self):
		m = len(self.y)
		h = self.sigmoid(np.dot(self.X,self.theta))
		cost = (1/m)*(((-(self.y)).T @ np.log(h))-((1-self.y).T @ np.log(1-h)))
		return (cost)

	def gradient_descent(self):
		m = len(self.y)
		if m < 1:
			print("Not enough data")
			sys.exit(-1)
		cost_history = []
		for i in range(self.iterations):
			self.theta -= (self.learning_rate / m) * (np.dot(self.X.T, self.sigmoid((self.X @ self.theta)) - self.y))
			cost = self.cost()[0][0]
			if (len(cost_history) > 0):
				delta = cost_history[-1] - cost
				if ((delta < 0.000001 and self.learning_rate > 0.0001 and cost < cost_history[-1]) or cost > cost_history[-1]):
					self.learning_rate /= 2
				if (delta < 1e-10):
					cost_history.append(cost)
					break
			cost_history.append(cost)
			if cost < 0.02:
				cost_history.append(cost)
				break
		return(cost_history)