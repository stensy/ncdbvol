"""

ncdbvol.py

Using the ncdbwithlabels.csv file, calculate hospital volume using the
PUF ID. 

Will utilize a file classifying the cystectomy codes for volume definition.

"""

import csv
import operator

## create a list for the cystectomy codes
cystlist = []
with open('cystcodes.csv', 'rU') as cystdictin:
	cystreader = csv.reader(cystdictin)
	for line in cystreader:
		cystlist.append(line[0])

print cystlist

## create a dictionary for volume at each facility
## should result with facvol which is a dict with yearly facility cx volume
## and totfacvol which is a dict with total facility cx volume

### facility ID is in column 1 (0 indexed)
### year of DX is in column 16 (0 indexed)
### surgery code is in column 79 (0 indexed)

facvol = {}
totfacvol = {}

totalcysts = 0

with open('ncdbnolabels.csv', 'rU') as ncdbin:
	ncdb = csv.reader(ncdbin)
	ncdb.next()
	for row in ncdb:
		if row[79] in cystlist:
			totalcysts += 1
			try:
				totfacvol[row[1]] += 1
			except:
				totfacvol[row[1]] = 1

			try:
				facyear = str(row[16]) + str(row[1])
				try:
					facvol[facyear] += 1
				except:
					facvol[facyear] = 1
			except:
				pass

with open('ncdbwithlabels.csv', 'rU') as infile:
	ncdb = csv.reader(infile)
	headerrow = ncdb.next()
	with open('ncdbwithlabels_volume.csv', 'w') as outfile:
		ncdbout = csv.writer(outfile)
		headerrow.extend(['hosp_year_vol', 'hosp_tot_vol'])
		ncdbout.writerow(headerrow)
		for row in ncdb:
			try:
				row.extend([facvol[(str(row[16]) + str(row[1]))], totfacvol[row[1]]])
			except:
				row.extend(['keyerror', 'keyerror'])
			ncdbout.writerow(row)

