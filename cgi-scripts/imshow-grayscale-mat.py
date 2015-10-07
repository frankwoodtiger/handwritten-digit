import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt

figureNum = 0

def getMNISTFromGrayscale(grayscaleImageData):
	lowerbound_mn = -1.0
	upperbound_mn = 1.0
	upperbound_gs = 255.0
	resolution = (upperbound_mn - lowerbound_mn) / upperbound_gs
	mnist_array = lowerbound_mn + grayscaleImageData * resolution
	return mnist_array

def getNormalizedMNist(mnist):
	return mnist.flattern()

def getMNISTSingleSampleByIndex(indx):
	X = sio.loadmat("ex4data1.mat")["X"]
	return np.transpose(np.reshape(X, (5000, 20, 20))[indx])
	
fileName = "grayscale.mat"
imageData = sio.loadmat(fileName)["grayscale"]
imageData_MNIST_formated = getMNISTFromGrayscale(imageData)

print imageData_MNIST_formated
plt.figure(figureNum)
plt.imshow(imageData_MNIST_formated, cmap=plt.cm.Greys, interpolation='none')

MNIST_sample = getMNISTSingleSampleByIndex(3500)
print MNIST_sample
figureNum = figureNum + 1
plt.figure(figureNum)
plt.imshow(MNIST_sample, cmap=plt.cm.Greys, interpolation='none')

plt.show()