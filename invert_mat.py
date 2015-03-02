__Author__="Yuncheng Mao"
__Email__='''catmyc@gmail.com; maoyuncheng@mail.nankai.edu.cn'''

'''
For transvert the matrix recorded in a text file
'''

class invertor:
	'''
	For transvese the matrix recorded in a text file.
	I think the computer is able to handle the operation within memory.
	'''
	started = False
	num_records = 0
	matrix = [] # Uninitialized matrix
	def __init__(self, filename):
		print('-' * 15 + '> START <' + '-' * 15)
		for line in open(filename, 'r'):
			tempBuff = line.split()
			# convert to a float list
			buff = []
			for f in tempBuff:
				buff.append(float(f))
			
			if not self.started: # Meaning reading first line
				print("INFO: Initializing the data matrix!!!")
				self.num_records = len(buff)
				self.started = True
				print("INFO: The trajectories of %d coordinates are recorded." % self.num_records)
				# initialize an empty matrix (2D list array)
				for i in range(self.num_records):
					# initialize and append the first line of data into matrix
					self.matrix.append([buff[i]])
			else:
				for i in range(len(buff)):
					self.matrix[i].append(buff[i])
		self.writeToFile("trans_" + filename)
		print('-' * 15 + '> END <' + '-' * 15)
	
	def writeToFile(self, filename):
		outfil = open(filename, 'w')
		print("INFO: Opened file %s for writing." % filename)
		for l in self.matrix:
			outline = ("%6.3f " * len(l) + "\n") % tuple(l)
			outfil.write(outline)
		outfil.close()
		print("INFO: Writing file %s finished." % filename)

# Execution
inv = invertor(r'min_dist_pbc_coor_chol.dat')
inv = invertor(r'min_dist_pbc_coor_lip.dat')

