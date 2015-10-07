#!C:\Python27\python
# Import modules for CGI handling 
import cgi, cgitb 
import sys, json

# import modules for math calculation of Neural Network
import numpy as np
import scipy.io as sio
from random import randint
import sys

# This activates a special exception handler that will display detailed reports in the Web
# browser if any errors occur.
cgitb.enable()

# Instantiate it exactly once, without arguments. This reads the form contents from standard 
# input or the environment. The FieldStorage instance can be indexed like a Python dictionary.
# And data will be in the following dict format:
# FieldStorage(None, None, [MiniFieldStorage('imageData', 
# 	'{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8" ...
# with key as index of the pixel and value as the pixel value (0 to 255)
data = cgi.FieldStorage()

imageData_str = data['imageData_gs_1d'].value
imageData_list = json.loads(imageData_str) # decoding JSON string
imageData_nparray = np.array(imageData_list).reshape(28, 28)

print "Content-Type: text/plain\n"
# print imageData_list
print imageData_nparray

sio.savemat('grayscale.mat', dict(grayscale=imageData_nparray))