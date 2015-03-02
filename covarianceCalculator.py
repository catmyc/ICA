#!/usr/bin/env python3

__Author__ = "Yuncheng Mao"
__Email__ = '''catmyc@gmail.com; maoyuncheng@mail.nankai.edu.cn'''

'''
1 calculate the colvariance matrix from standardized data;
2 calculate the time-lagged colvariance matrix from standardized data.
'''

from vector import *
import time

def emptyMat(nrow):
	mat = []
	for i in range(nrow):
		mat.append([])
	return mat

def zeroMat(nrow, ncol):
	zeroMat = emptyMat(nrow)
	for i in range(nrow):
		for j in range(ncol):
			zeroMat[i].append(0)
	return zeroMat

class ICA:
	data = []
	nframes = 0
	ncoors = 0
	timeLag = 0
	CV = [] # covariance matrix
	CVT = [] # time-lagged covariance matrix

	def __init__(self, filename, timelag):
		'''
		Read in data and initialize empty matrices
		'''
		infil = open(filename, 'r')
		line = infil.readline()
		line = line.split()
		self.nframes = len(line)
		print('INFO: Data containing %d frames.' % self.nframes)
		infil.close()
		with open(filename) as infil:
			self.ncoors = sum(1 for x in infil)
		print('INFO: Data containing %d coordinates, i.e. %d atoms.' % (self.ncoors, self.ncoors / 3))
		print('INFO: Initializing empty matrices...')
		self.CV = zeroMat(self.ncoors, self.ncoors)
		self.CVT = zeroMat(self.ncoors, self.ncoors)
		print('INFO: Reading data from file %s...' % filename)
		for line in open(filename):
			buff = line.split()
			newBuff = []
			for f in buff:
				newBuff.append(float(f))
			self.data.append(newBuff)
		print('INFO: Readin finished.')
		self.calcCV()
		self.writeMatrix(self.CV, 'covariance.dat')
		self.calcCVT(timelag)
		self.writeMatrix(self.CVT, 'time-lagged_covariance.dat')
		print('=' * 35)
	# calcCV and calcCVT requires heavy loads of computations...
	def calcCV(self):
		'''
		calculate the covariance matrix.
		'''
		print('INFO: Calculating the covariance matrix...')
		t_beg = time.time()
		workCounter = 0
		total = self.ncoors ** 2
		for i in range(self.ncoors):
			veci = self.data[i]
			for j in range(i, self.ncoors):
				vecj = self.data[j]
				product = vecdot(self.data[i], self.data[j]) / self.nframes
				self.CV[i][j] = product
				if i != j:
					self.CV[j][i] = product
				workCounter += 2
				if workCounter % 10000 == 0:
					print("%5.2f%% done." % (workCounter / total * 100))
		print('INFO: Covariance matrix done.')
		print('INFO: Calculation finished in %d seconds.' % (time.time() - t_beg))


	def calcCVT(self, tlag):
		'''
		calculate the time-lagged covariance matrix
		It's much more time-consuming than calcCV.
		'''
		print('INFO: Calculating the time-lagged covariance matrix...')
		t_beg = time.time()
		print('INFO: The time lag is %d frames!!!' % tlag)
		workCounter = 0
		total = self.ncoors ** 2
		for i in range(self.ncoors):
			veci = self.data[i][0:(self.nframes - tlag)]
			vecii = self.data[i][tlag:]
			for j in range(self.ncoors):
				vecj = self.data[j][tlag:]
				vecjj = self.data[j][0:(self.nframes - tlag)]
				p = vecdot(veci, vecj) / (self.nframes - tlag)
				pp = vecdot(vecii, vecjj) / (self.nframes - tlag)
				product = 0.5 * (p + pp)
				self.CVT[i][j] = product
				if i != j:
					self.CVT[j][i] = product
				workCounter += 2
				if workCounter % 10000 == 0:
					print("%5.2f%% done." % (workCounter / total * 100))
		print('INFO: Time-lagged covariance matrix done.')
		print('INFO: Calculation finished in %d seconds.' % (time.time() - t_beg))
	
	def writeMatrix(self, mat, filename):
		print('INFO: Writing to file %s...' % filename)
		ofil = open(filename, 'w')
		counter = 0
		for l in mat:
			line = ("%8.5f " * len(l) + "\n") % tuple(l)
			ofil.write(line)
			counter += 1
		ofil.close()
		print("INFO: %d lines written." % counter)

#####################
# Execution
#####################
from sys import argv
datafile = argv[1]
timelag = int(argv[2])
cvCal = ICA(datafile, timelag)


