'''

ncdbrprocessing.py

Further processing of the file ncdbwithlabels_volume_out.csv.

Corresponds to the steps outlined in ncdb_processing_steps.txt

'''

import csv
import operator
import numpy as np

totalcysts = 0
totalcases = 0
cystectomies = 0
path_included = 0
cut_cystectomies = 0
cut_pathology = 0
sequence_included = 0
sequence_cut = 0
histology_included = 0
histology_cut = 0
radiation_included = 0
radiation_cut = 0
mortality_included = 0
mortality_cut = 0
chemo_included = 0
chemo_cut = 0
adjuvant_included = 0
adjuvant_cut = 0
no_chemo = 0
no_chemo_2 = 0
got_chemo = 0
included_cases = 0
missing_post_surg_timing = 0
facvolerrors = 0

cystlist = []
included_path_t = []
included_path_n = []
histlist = []

totfacvol = {}
facyrvol = {}
facmedians = {}
sequence_dict = {}

with open('cystcodes.csv', 'rU') as cystdictin:
	print "Creating cystectomy code list."
	cystreader = csv.reader(cystdictin)
	cystreader.next()
	for line in cystreader:
		cystlist.append(line[0])

with open('included_path_t.csv', 'rU') as pathtdictin:
	print "Creating path_t code list."
	pathreader = csv.reader(pathtdictin)
	pathreader.next()
	for line in pathreader:
		included_path_t.append(line[0])

with open('included_path_n.csv', 'rU') as pathndictin:
	print "Creating path_n code list."
	pathreader = csv.reader(pathndictin)
	pathreader.next()
	for line in pathreader:
		included_path_n.append(line[0])

with open('included_hist.csv', 'rU') as histdictin:
	print "Creating histology code list."
	histreader = csv.reader(histdictin)
	histreader.next()
	for line in histreader:
		histlist.append(line[0])

with open('ncdbr.csv', 'rU') as ncdbin:
	print "Reading NCDB file and writing volume dictionaries."
	ncdb = csv.reader(ncdbin)
	ncdb.next()
	for row in ncdb:
		if int(row[16]) > 2006:
			pass
		else: 
			if row[76] in cystlist:
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
	facmedians[fac] = mediancysts

ncdbvars = []
newheaderrow = []
with open('ncdb_variables.csv', 'rU') as infile:
	varread = csv.reader(infile)
	varread.next()
	for row in varread:
		ncdbvars.append((row[0],row[1]))
		newheaderrow.append(row[1])


with open('ncdbr.csv', 'rU') as infile:
	ncdb = csv.reader(infile)
	with open('ncdbr_processed.csv', 'w') as outfile:
		ncdbout = csv.writer(outfile)
		newheaderrow.extend(['fac_cx_vol', 'adjuvant_chemo', 'days_adjuvant_chemo'])
		ncdbout.writerow(newheaderrow)
		for row in ncdb:
			totalcases += 1

			## Only include radical cystectomies
			if row[76].strip() in cystlist:
				cystectomies += 1
			else:
				cut_cystectomies += 1
				continue

			## Only include >= pT3 or N+
			if row[32].strip() in included_path_t or row[33].strip() in included_path_n:
				path_included += 1
			else:
				cut_pathology += 1
				continue

			## Only include transitional cell carcinoma
			if row[19].strip() in histlist:
				histology_included += 1
			else:
				histology_cut += 1
				continue

			## Only include cases with NO radiation
			if row[85].strip() == '0':
				radiation_included += 1
			else:
				radiation_cut += 1
				continue
			
			## Only include cases if patient survived 30 days
			if row[109].strip() == '0':
				mortality_included += 1
			else:
				mortality_cut += 1
				continue

			## Only include cases if patient received NO or ADJUVANT chemo
			if row[98].strip() == '00':
				chemo_included += 1
				no_chemo += 1
				adjuvant_chemo = 0
				days_adjuvant_chemo = 'NULL'
			else:
				try:
					## Calculate days from definitive surgery (row[75]) to chemo (row[97])
					days_adjuvant_chemo = int(row[97]) - int(row[75])
				except:
					days_adjuvant_chemo = 9999

				if days_adjuvant_chemo > 0 and days_adjuvant_chemo <= 90:
					adjuvant_included += 1
					adjuvant_chemo = 1
				else:
					adjuvant_cut += 1
					continue

			## Only include primary cancer site
			try:
				sequence_dict[row[14]] += 1
			except:
				sequence_dict[row[14]] = 1

			if row[14].strip() == "00":
				sequence_included += 1
			else:
				sequence_cut += 1
				continue

			included_cases += 1
			try:
				facvol = facmedians[row[1]]
			except:
				facvol = 'ERROR IN VOL CALC'
				facvolerrors += 1

			newrow = []
			for (colIndex, varname) in ncdbvars:
				newrow.append(row[int(colIndex)])

			newrow.extend([facvol, adjuvant_chemo, days_adjuvant_chemo])
			ncdbout.writerow(newrow)

print "Total number of cases was: ", totalcases
print "Total number of CUTS at cystectomy was: ", cut_cystectomies
print "Total number of cystectomies was: ", cystectomies
print "Total number of CUTS at pathology was: ", cut_pathology
print "Total number of included pathologies was: ", path_included
print "Total number of CUTS at histology was: ", histology_cut
print "Total number included for TCC was: ", histology_included
print "Total number of CUTS at radiation was: ", radiation_cut
print "Total number included for no radiation was: ", radiation_included
print "Total number of CUTS at mortality was: ", mortality_cut
print "Total number included for mortality was: ", mortality_included
print "Total number of CUTS for chemo timing was: ", adjuvant_cut
print "Number of patients NOT receiving chemo after cystectomy was: ", no_chemo
print "Total number of patients included after adjuvant cut was: ", adjuvant_included
print "Total number included at cancer sequence was: ", sequence_included
print "Total number of CUTS at cancer sequence was: ", sequence_cut
print "Final number of included cases was: ", included_cases
print "Total cases was %i, computed cases from cuts and included cases is %i." % (totalcases, included_cases + cut_cystectomies + cut_pathology + sequence_cut + histology_cut + radiation_cut + mortality_cut + chemo_cut + adjuvant_cut)

print "Values for SEQUENCE_NUMBER were as follows:"
print sequence_dict

print "Number of facvol errors: ", facvolerrors