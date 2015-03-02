from sys import argv
filename = argv[1]
print("INFO: Opened file %s for reading." % filename)
outfil = open('reformated_' + filename, 'w')
print("INFO: Opened file %s for writing." % ('reformated_' + filename))
for line in open(filename, 'r'):
	buff = line.split()
	newBuff = []
	for f in buff:
		newBuff.append(float(f))
	outline = ("%6.3f " * len(newBuff) + "\n") % tuple(newBuff)
	outfil.write(outline)
print("INFO: reading finished.")
print("INFO: writing finished.")
outfil.close()
print('-' * 15 + '> END <' + '-' * 15)

