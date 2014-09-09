"""

ncdbvol.py

Using the ncdbwithlabels.csv file, calculate hospital volume using the
PUF ID. 

Will utilize a file classifying the cystectomy codes for volume definition.

"""

import csv
import operator
import numpy as np

## create a list for the cystectomy codes
cystlist = []
with open('cystcodes.csv', 'rU') as cystdictin:
	print "Creating cystectomy code list."
	cystreader = csv.reader(cystdictin)
	for line in cystreader:
		cystlist.append(line[0])

## create dictionaries for volume at each facility
## will result with facvol which is a dict with yearly facility cx volume
### totfacvol which is a dict with total facility cx volume
### facyrvol which is a dict of dicts giving annual volume for each facility 1998-2006

### facility ID is in column 1 (0 indexed)
### year of DX is in column 16 (0 indexed)
### surgery code is in column 79 (0 indexed)

totfacvol = {}
facyrvol = {}
medians = {}

totalcysts = 0

with open('ncdbnolabels.csv', 'rU') as ncdbin:
	print "Reading NCDB file and writing volume dictionaries."
	ncdb = csv.reader(ncdbin)
	ncdb.next()
	for row in ncdb:
		if int(row[16]) > 2006:
			pass
		else: 
			if row[79] in cystlist:
				totalcysts += 1
				try:
					totfacvol[row[1]] += 1
				except:
					totfacvol[row[1]] = 1

				try:
					facyrvol[row[1]][row[16]] += 1
				except:
					facyrvol[row[1]] = {'1998': 0, '1999': 0, '2000': 0, '2001': 0, 
						'2002': 0, '2003': 0, '2004': 0, '2005': 0, '2006': 0}
					facyrvol[row[1]][row[16]] += 1

## Calculate the median volume for each facility from 1998-2006 
## and write it to a dictionary
print "Calculating median cystectomy volume values."
for fac, facdict in facyrvol.items():
	mediancysts = np.median(facdict.values())
	medians[fac] = mediancysts

ncdbvars = []
headerrow = []
with open('ncdb_variables.csv', 'rU') as infile:
	varread = csv.reader(infile)
	varread.next()
	for row in varread:
		ncdbvars.append((row[0],row[1]))
		headerrow.append(row[1])

with open('ncdbnolabels.csv', 'rU') as infile:
	print "Writing calculated values to outfile."
	ncdb = csv.reader(infile)
	ncdb.next()
	with open('ncdbnolabels_volume_out.csv', 'w') as outfile:
		ncdbout = csv.writer(outfile)
		ncdbout.writerow(headerrow)
		for row in ncdb:
			rowlist = []
			for (colindex, varname) in ncdbvars:
				rowlist.append(row[int(colindex)])
			ncdbout.writerow(rowlist)