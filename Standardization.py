#!/usr/bin/env python3

'''
Use this code instead of the ICA_prepare.tcl to achieve better efficiency!
'''
__Author__ = "Yuncheng Mao"
__Email__ = "catmyc@gmail.com; maoyuncheng@mail.nankai.edu.cn"

from vector import *
from sys import argv

filename = argv[1]
outfilename = "stand_" + filename

print("-" * 25 + "> START <" + "-" * 25)

print("INFO: Opened file %s to read." % filename)
print("INFO: Will write to file %s." % outfilename)

ofil = open(outfilename, 'w')

counter = 0
num_per_line = 0
for line in open(filename, 'r'):
	counter += 1
	if counter % 50 == 0:
		print("INFO: %d lines read!" % counter)
	buff = line.split()
	if counter == 1:
		num_per_line = len(buff)
		print("INFO: Each line contains %d records!" % num_per_line)
	vec = []
	for f in buff:
		vec.append(float(f))
	#vstd = vec_standardized(vec)
	outputline = ("%8.5f " * num_per_line + "\n") % tuple(vec_standardized(vec))
	ofil.write(outputline)
print("Summary: %d lines processed!" % counter)
print("-" * 25 + "> END <" + "-" * 25)


