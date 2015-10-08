#!C:\Python27\python
# Import modules for CGI handling 
import cgi, cgitb 

# import modules for math calculation of Neural Network
import numpy as np
import scipy.io as sio
from random import randint
import sys, struct, json
from array import array

import matplotlib.pyplot as plt # need to comment out for CGI

class MachineLearning:
	figureNum = 0
	EPSILON = 0.08 # sqrt(6 / (784 + 10)
	lambda_reg = 1          # for regularization term
	learningRate = 0.03
	input_layer_size  = 784 # 28x28 Input Images of Digits with 5000 training sample
	hidden_layer_size = 25  # 25 hidden units
	output_layer_size = 10
	num_labels = 10         # 10 labels, from 0 to 9   
	
	def readMat(self, fileName):
		return sio.loadmat(fileName)
	
	def displayCostVsIter(self, J_array):
		max_cost = J_array.max()
		min_cost = J_array.min()
		delta = J_array[-1] - J_array[0]
		delta_percent = (delta / J_array[0])*100
		print 'max cost: {:.9f}\nmin cost: {:.9f}\ndelta: {:.9f}\ndelta %: {:.9f}%'.format(max_cost, min_cost, delta, delta_percent)
		self.figureNum = self.figureNum + 1
		plt.figure(self.figureNum)
		# print J_array
		plt.plot(J_array)
		plt.ylabel('J(theta)')
	
	def showAllGraphs(self):
		plt.show()
		
	def load_mnist(self, dataset="training", digits=np.arange(10), path="."):
		"""
		Loads MNIST files into 3D numpy arrays

		Adapted from: http://abel.ee.ucla.edu/cvxopt/_downloads/mnist.py
		"""

		if dataset == "training":
			fname_img = 'train-images.idx3-ubyte'
			fname_lbl = 'train-labels.idx1-ubyte'
		elif dataset == "testing":
			fname_img = 't10k-images.idx3-ubyte'
			fname_lbl = 't10k-labels.idx1-ubyte'
		else:
			raise ValueError("dataset must be 'testing' or 'training'")

		flbl = open(fname_lbl, 'rb')
		magic_nr, size = struct.unpack(">II", flbl.read(8))
		lbl = array("b", flbl.read())
		flbl.close()

		fimg = open(fname_img, 'rb')
		magic_nr, size, rows, cols = struct.unpack(">IIII", fimg.read(16))
		img = array("B", fimg.read())
		fimg.close()

		ind = [ k for k in range(size) if lbl[k] in digits ]
		N = len(ind)

		images = np.zeros((N, rows, cols), dtype=np.uint8)
		labels = np.zeros((N, 1), dtype=np.int8)
		for i in range(len(ind)):
			images[i] = np.array(img[ ind[i]*rows*cols : (ind[i]+1)*rows*cols ]).reshape((rows, cols))
			labels[i] = lbl[ind[i]]

		return images, labels
		
	def setEPSILON(self, Linput, Loutput):
		# 6.0 is important here as it make the expression as float
		self.EPSILON = np.sqrt(6.0 / (Linput + Loutput))
		
	def sigmoid(self, z):
		return 1.0 / (1.0 + np.exp(-z))
	
	def linearCombo(self, theta, X):
		# Theta1: 25x785
		# X: 785x1
		return theta.dot(X)
		
	def computeActivation(self, a_vector, theta):
		z = self.linearCombo(theta, a_vector)
		return self.sigmoid(z)
		
	# we have 1 hidden layer. Hence, we have theta1 and theta2
	def costFunction(self, X, y, theta1, theta2, debug):
		m = X.shape[0]
		J = 0
		X_b = np.append(np.ones((X.shape[0],1)), X, 1) # add bias term in the input vectors
		THETA1_grad = np.zeros(theta1.shape)
		THETA2_grad = np.zeros(theta2.shape)
		for i in range(0, m):
			# forward propagation
			a1 = np.reshape(X_b[i], (X_b[i].shape[0],1)) # transform from (401,) to (401,1) dimension-wise
			a2 = self.sigmoid(self.linearCombo(theta1, a1))
			a2 = np.append(1, a2)                        # append bias term in a2
			a2 = np.reshape(a2, (a2.shape[0], 1))        # transform from (26,) to (26,1) dimension-wise
			h = self.sigmoid(self.linearCombo(theta2, a2))
			
			# transform the y vector be logical vector
			y_vec = np.zeros((self.num_labels, 1)) # 10 x 1
			y_vec[y[i][0]] = 1 # since y fetched from MNIST is from 0 to 9, no offset is needed
			
			# back propagation 
			d3 = h - y_vec
			d2 = np.multiply(theta2.T.dot(d3), np.multiply(a2, 1-a2))
			THETA2_grad = THETA2_grad + d3.dot(a2.T)
			THETA1_grad = THETA1_grad + d2[1:].dot(a1.T)
			
			# Compute cost: J(theta)
			J = J + np.sum(np.multiply(y_vec, np.log(h)) + np.multiply(1 - y_vec, np.log(1 - h)))
			
			if debug == True and i == 0:
				print 'dim(a1): {}'.format(a1.shape)
				# print a1
				print 'dim(a2): {}'.format(a2.shape)
				# print a2
				print 'dim(h): {}'.format(h.shape)
				# print h
				print 'dim(y_vec): {}'.format(y_vec.shape)
				print y[i]
				print y_vec
				print d3
				print y_vec - d3
				
			# non-vectorized implementation
			# for k in range(0, self.num_labels):
			# 	J = J + y_vec[k]*np.log(h[k]) + (1-y_vec[k])*np.log(1-h[k])
		
		# add the regularization term (3 layers implementation)
		regTerm = 0
		for j in range(theta1.shape[0]):
			for k in range(theta1.shape[1]-1): # ignoring bias
				regTerm = regTerm + np.power(theta1[j,k+1], 2)
		for j in range(theta2.shape[0]):
			for k in range(theta2.shape[1]-1): # igno1ring bias
				regTerm = regTerm + np.power(theta2[j,k+1], 2)
		regTerm = self.lambda_reg*regTerm/(2*m)
		J = -1.0 * J/m + regTerm
		
		# calculate theta term for further gradient descent/optimization term
		reg_grad_1 = np.multiply(self.lambda_reg, theta1)
		reg_grad_1[:,0] = 0
		THETA1_grad = np.divide(THETA1_grad + reg_grad_1, m)
		
		reg_grad_2 = np.multiply(self.lambda_reg, theta2)
		reg_grad_2[:,0] = 0
		THETA2_grad = np.divide(THETA2_grad + reg_grad_2, m)
		
		if debug == True:
			print 'dim(THETA1_grad): {}'.format(THETA1_grad.shape)
			print 'dim(THETA2_grad): {}'.format(THETA2_grad.shape)
				
		
		# return a Python dict with all parameters
		return {
			'J': J,
			'THETA1_grad': THETA1_grad,
			'THETA2_grad': THETA2_grad
		}
	
	def trainNN(self, X, y, iter, isThetaExist):
		m = X.shape[0]
		J_array = np.zeros((iter,))
		
		# see if there are old thetas to use
		if isThetaExist == True:
			thetaDict = self.readMat('thetas.mat')
			theta1 = thetaDict['theta1']
			theta2 = thetaDict['theta2']
		else:
			self.setEPSILON(self.input_layer_size, self.output_layer_size)
			print "EPSILON = {:.9f}".format(self.EPSILON)
			theta1 = 2*self.EPSILON*np.random.random((self.hidden_layer_size,self.input_layer_size + 1)) - self.EPSILON # 784 input, 25 hidden unit, 10 output
			theta2 = 2*self.EPSILON*np.random.random((self.output_layer_size,self.hidden_layer_size + 1)) - self.EPSILON # 784 input, 25 hidden unit, 10 output
			# dim(theta2) = 10x26
			# dim(theta1) = 25x785
			
		for i in range(iter):
			print i
			# gradient descent
			dataSet = self.costFunction(X, y, theta1, theta2, False)
			J_array[i] = dataSet['J']
			# print J_array[i]
			THETA1_grad = dataSet['THETA1_grad']
			THETA2_grad = dataSet['THETA2_grad']
			theta1 = theta1 - np.multiply(self.learningRate, THETA1_grad)
			theta2 = theta2 - np.multiply(self.learningRate, THETA2_grad)
		
		if (J_array[-1] - J_array[0]) < 0:
			self.saveMat('thetas.mat', theta1, theta2)
		else:
			print 'cost is increasing'
			
		# return a Python dict with all parameters
		return {
			'J_array': J_array,
			'theta1': theta1,
			'theta2': theta2
		}
			
	
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
			# no offset is needed if data is fetched from load_mnist
			p[i] = np.argmax(h2)
		return p
	
	# prediction over a single sample, it's actually a feed forward step
	def singlePredict(self, theta1,  theta2, x):
		x_b = np.append(1, x)
		h1 = self.sigmoid(self.linearCombo(theta1, x_b))
		h1 = np.append(1, h1)
		h2 = self.sigmoid(self.linearCombo(theta2, h1))
		# no offset is needed if data is fetched from load_mnist
		return np.argmax(h2) 
	
	def measureAccurancy(self, theta1, theta2, X, y):
		p = self.batchPredict(theta1, theta2, X) # (m, 1=num_labels) e.g (5000, 10)
		print "p.shape: {}".format(p.shape)
		print "y.shape: {}".format(y.shape)
		print "p.min: {}".format(p.min())
		print "p.max: {}".format(p.max())
		print "y.min: {}".format(y.min())
		print "y.max: {}".format(y.max())
		return np.mean(p == y)*100
	
	def saveMat(self, filename, theta1, theta2):
		sio.savemat(filename, dict(theta1=theta1, theta2=theta2))
		
if __name__=='__main__':
	cgitb.enable()
	data = cgi.FieldStorage()
	# iter = int(data['iter'].value)
	
	ml = MachineLearning()
	
	images_t, labels_t = ml.load_mnist('testing')
	X_t = np.reshape(images_t, (10000, 784)).astype(float)
	y_t = labels_t.astype(float)
	
	images, labels = ml.load_mnist('training')
	# image is 60000 x 28 x 28 data
	# labels is 60000 x 1
	
	X = np.reshape(images[0:5000], (5000, 784)).astype(float) # 5000 x 784
	y = labels[0:5000].astype(float) # 5000 x 1
	
	# X = np.reshape(images, (60000, 784)) # 60000 x 784
	# y = labels # 60000 x 1
	
	# dataSet = ml.trainNN(X, y, iter, False) # used for the first time to generate thetas
	dataSet = ml.trainNN(X, y, 10, True)
	accurancyStr = 'With Weight trained from scratch: {}% accurancy'.format(ml.measureAccurancy(dataSet['theta1'], dataSet['theta2'], X_t, y_t))
	J_array =  dataSet['J_array']
	ml.displayCostVsIter(J_array)
	
	print "Content-Type: text/plain;charset=utf-8\r\n" 
	print accurancyStr
	# print X.min()
	# print X.max()
	# print y.min()
	# print y.max()
	
	ml.showAllGraphs()