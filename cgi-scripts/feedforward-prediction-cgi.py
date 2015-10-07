#!C:\Python27\python
# Import modules for CGI handling 
import cgi, cgitb 

# import modules for math calculation of Neural Network
import numpy as np
import scipy.io as sio
from random import randint
import sys, json

class MachineLearning:
	figureNum = 0 
	
	def readMat(self, fileName):
		return sio.loadmat(fileName)
		
	def sigmoid(self, z):
		return 1.0 / (1.0 + np.exp(-z))
	
	def linearCombo(self, theta, X):
		# Theta1: 25x401
		# X: 401x1
		return theta.dot(X)
		
	# X is a matrix with multiple samples (row per sample)
	def batchPredict(self, theta1, theta2, X):
		m = X.shape[0]
		num_labels = theta2.shape[0]
		
		p = np.zeros((m,1))
		X_b = np.append(np.ones((m,1)), X, 1)
		for i in range(m):
			h1 = self.sigmoid(self.linearCombo(theta1, X_b[i]))
			h1 = np.append(1, h1)
			h2 = self.sigmoid(self.linearCombo(theta2, h1))
			# take the index of max value, which is the actual value
			# note that y is matrix with value from 1 to 10, neet to take the offset
			p[i] = np.argmax(h2) 
		return p
	
	# prediction over a single sample, it's actually a feed forward step
	def singlePredict(self, theta1,  theta2, x):
		x_b = np.append(1, x)
		h1 = self.sigmoid(self.linearCombo(theta1, x_b))
		h1 = np.append(1, h1)
		h2 = self.sigmoid(self.linearCombo(theta2, h1))
		return np.argmax(h2) 
	
	def measureAccurancy(self, theta1, theta2, X, y):
		p = self.batchPredict(theta1, theta2, X) # (m, 1=num_labels) e.g (5000, 10)
		return np.mean(p == y)*100
	
	def saveMat(self, theta1, theta2):
		sio.savemat('theta.mat', dict(theta1=theta1, theta2=theta2))
	
	def getMNISTFromGrayscale(self, grayscaleImageData):
		lowerbound_mn = -1.0
		upperbound_mn = 1.0
		upperbound_gs = 255.0
		resolution = (upperbound_mn - lowerbound_mn + 1) / upperbound_gs
		mnist_array = lowerbound_mn + grayscaleImageData * resolution
		return mnist_array
		
if __name__=='__main__':
	cgitb.enable()
	data = cgi.FieldStorage()
	imageData_str = data['imageData_gs_1d'].value
	imageData_list = json.loads(imageData_str) # decoding JSON string
	imageData_nparr = np.array(imageData_list)
	
	ml = MachineLearning()
	imageWeight = ml.readMat('thetas.mat')
	Theta1 = imageWeight['theta1']
	Theta2 = imageWeight['theta2']
	
	predict = ml.singlePredict(Theta1, Theta2, imageData_nparr)
	
	print "Content-Type: text/plain;charset=utf-8\r\n" 
	print predict