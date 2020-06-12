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
		h = self.sigmoid(np.dot(self.X,self.theta))
		cost = (1/m)*(((-(self.y)).T @ np.log(h))-((1-self.y).T @ np.log(1-h)))
		return (cost)

	def gradient_descent(self):
		m = len(self.y)
		cost_history = []
		for i in range(self.iterations):
			self.theta = self.theta - (self.learning_rate / m) * (np.dot(self.X.T, self.sigmoid((self.X @ self.theta)) - self.y))
			cost = self.cost()
			# print(cost)
			if cost[0][0] > 0.1:
				cost_history.append(cost[0][0])
			else :
				print("fin", i)
				break
		return(cost_history)