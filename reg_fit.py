import numpy as np

class regression:

	def __init__(self, X, y, theta, learning_rate, iterations):
		self.X = X
		self.y = y
		self.theta = theta
		self.learning_rate = learning_rate
		self.iterations = iterations
	 

	def sigmoid(self, z):
		return (1 / (1 + np.exp(-z)))

	def predict(self):
		return(sigmoid(np.dot(self.X, self.theta)))

	def cost(self):
		m = len(self.y)
		y = self.y.T
		h = self.sigmoid(np.dot(self.X, self.theta))
		cost = (1 / m) * ((np.dot(y, np.log(h))) + np.dot((1 - y), np.log(1-h)))
		return (cost)

	def gradient_descent(self):
		m = len(self.y)
		cost_history = np.zeros((self.iterations, 1))
		for i in range(self.iterations):
			self.theta = self.theta - (self.learning_rate / m) * (np.dot(self.X.T, self.sigmoid((self.X @ self.theta)) - self.y))
			cost_history[i] = self.cost()
		return(cost_history, self.theta)