__Author__ = '''
             Yuncheng Mao
		   	 '''
__Email__ = '''catmyc@gmail.com
            maoyuncheng@mail.nankai.edu.cn
		    '''

import math

def vecadd(vec1, vec2):
	if len(vec1) == len(vec2):
		newVec = []
		for i in range(len(vec1)):
			a = vec1[i] + vec2[i]
			newVec.append(a)
		return newVec
	else:
		print("ERROR: Two vectors must be of equal length!!!")
		return None
def vecinv(vec):
	v = []
	for f in vec:
		v.append(-f)
	return v

def vecsub(vec1, vec2): # return vec1 - vec2
	vec2 = vecinv(vec2)
	return vecadd(vec1, vec2)

def vecdot(vec1, vec2):
	if len(vec1) == len(vec2):
		listForSum = []
		for i in range(len(vec1)):
			a = vec1[i] * vec2[i]
			listForSum.append(a)
		return math.fsum(listForSum)
	else:
		print("ERROR: Two vectors must be of equal length!!!")
		return None

def veclen(vec):
	return math.sqrt(vecdot(vec, vec))

def vecdist(vec1, vec2):
	return veclen(vecsub(vec1, vec2))


class coorTrajProcessor:
	'''
	For processing recorded coordinates of cholesterol and lipids according to the PBC.
	And rewrite the trajectory of each molecules in each line in temporal order.
	'''
	num_coors = 0 # set to 0, as a flag indicating having not read any data
	num_frames = 0
	refCoors = []

	def __init__(self, filename): # Reading file
		'''
		Note that the first TWO columns are the PBC dimensions in X and Y direction.
		The latter columns are the coordinates of each molecule.
		'''

		print("-"*15 + "> START <" + "-"*15)
		print("INFO: Opening file %s to read..." % filename)
		outfilename = "min_dist_" + filename
		print("INFO: Will write to file %s." % outfilename)
		print("INFO: The PBC data is dropped in output.")
		ofil = open(outfilename, 'w')
		for line in open(filename, 'r'):
			buff = line.split() # All data are stored as text.
			newBuff = []
			for t in buff: # convert to float first
				newBuff.append(float(t))
			self.num_frames += 1 # count how many frames are read.
			px = newBuff[0] # PBC X
			py = newBuff[1] # PBC Y
			del newBuff[0]
			del newBuff[1]
            # Construct a list of coordinates
			coorList = []
			j=0 #start
			while (j + 3) <= len(newBuff):
				coorList.append(newBuff[j:(j + 3)])
				j += 3

			# Safety Check
			if coorList[-1] != newBuff[-3:]:
				print("ERROR: The reformatted coordinate does not match the original data!!!")
				return -1
			# Starting Phase completed.

			# Processing starts...
			if self.num_coors == 0: 
				'''
				If reading the first line of data,
				record and use them as the reference frame.
				'''
				self.num_coors = len(coorList) # initialized
				self.refCoors = coorList.copy() # initialized
				print("INFO: %d coordinates recorded in this file." % self.num_coors)
			else: # Processing other lines of data
				for i in range(self.num_coors):
					# Replace each coordinate with the minimun distance image
					ref = self.refCoors[i]
					coor = coorList[i]
					images = self.imageCoors(px, py, coor)
					min_dist_coor = coor
					min_dist = vecdist(coor, ref)
					ifreplaced = False
					for c in images:
						dist = vecdist(c, ref)
						if dist <= min_dist:
							min_dist_coor = c
							min_dist = dist
							ifreplaced = True
					coorList[i] = min_dist_coor
                    # The next output is for debug...
					if ifreplaced:
						print("Replaced original coordiante with minimum-distance coordinate.")
					else:
						print("The original coordinate is the minimun-distance image!")
				    # Debug output finished

            # Construct an outputline
			outputline = []
			for f in coorList:
				outputline.extend(f)
			outputline = tuple(outputline)
			outBuff = ("%s " * len(outputline) + "\n") % outputline
			ofil.write(outBuff)
		ofil.close()
		print("INFO: Finished writing file %s." % outfilename)
		print("INFO: %d lines processed." % self.num_frames)
		print("-"*15 + "> END <" + "-"*15)

	def imageCoors(self, px, py, coor):
		'''
		The oder of the coordinates of the images in the returned result are stored in 
		the order as following:
		     2 -> 3 -> 4
		     /\        |
		     |         \/
		     1 <- O    5   /// O is the original coordinate
		               |
		               \/
		     8 <- 7 <- 6
		'''
		left = [-px, 0.0, 0.0]
		right = [px, 0.0, 0.0]
		up = [0.0, py, 0.0]
		down = [0.0, -py, 0.0]

		imageCoorList=[]
		image = coor
		for action in [left, up, right, right, down, down, left, left]:
			image = vecadd(image, action)
			imageCoorList.append(image)
		return imageCoorList

##############################
# Execution
##############################
from sys import argv
filename = argv[1]
worker = coorTrajProcessor(filename)

