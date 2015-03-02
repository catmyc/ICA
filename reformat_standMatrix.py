#!/usr/bin/env python3
from sys import argv
filename = argv[1]
print("INFO: Opened file %s for reading." % filename)
outfil = open('reformated_' + filename, 'w')
print("INFO: Opened file %s for writing." % ('reformated_' + filename))
lineCount = 0
for line in open(filename, 'r'):
	lineCount += 1
	if lineCount % 50 == 0:
		print("INFO: %d lines processed." % lineCount)
	buff = line.split()
	newBuff = []
	for f in buff:
		newBuff.append(float(f))
	outline = ("%12.9f " * len(newBuff) + "\n") % tuple(newBuff)
	outfil.write(outline)
print("INFO: reading finished.")
print("INFO: writing finished.")
outfil.close()
print("SUMMARY: Altogether %d lines processed!" % lineCount)
print('-' * 15 + '> END <' + '-' * 15)

