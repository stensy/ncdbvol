'''

ncdbprocessing.py

Further processing of the file ncdbwithlabels_volume_out.csv.

Corresponds to the steps outlined in ncdb_processing_steps.txt

'''

import csv

totalcases = 0
cystectomies = 0
path_included = 0
cut_cystectomies = 0
cut_pathology = 0
sequence_included = 0
sequence_cut = 0

cystlist = []
included_path_t = []
included_path_n = []

with open('cystcodes.csv', 'rU') as cystdictin:
	print "Creating cystectomy code list."
	cystreader = csv.reader(cystdictin)
	for line in cystreader:
		cystlist.append(line[0])

with open('included_path_t.csv', 'rU') as pathtdictin:
	print "Creating path_t code list."
	pathreader = csv.reader(pathtdictin)
	for line in pathreader:
		included_path_t.append(line[0])

with open('included_path_n.csv', 'rU') as pathndictin:
	print "Creating path_n code list."
	pathreader = csv.reader(pathndictin)
	for line in pathreader:
		included_path_n.append(line[0])


print included_path_t

print included_path_n

with open('ncdbnolabels_volume_out.csv', 'rU') as infile:
	ncdb = csv.reader(infile)
	headerrow = ncdb.next()
	with open('ncdb_processed.csv', 'w') as outfile:
		ncdbout = csv.writer(outfile)
		ncdbout.writerow(headerrow)
		for row in ncdb:
			totalcases += 1

			## Only include radical cystectomies
			if row[36] in cystlist:
				cystectomies += 1
			else:
				cut_cystectomies += 1
				continue

			## Only include >= pT3 or N+
			if row[29] in included_path_t or row[30] in included_path_n:
				path_included += 1
			else:
				cut_pathology += 1
				continue

			## Only include primary cancer site
			if row[14] == "00":
				sequence_included += 1
			else:
				sequence_cut += 1
				continue

			
			### MORE CUTS TO BE INSERTED HERE


			ncdbout.writerow(row)

print "Total number of cases was: ", totalcases
print "Total number of cystectomies was: ", cystectomies
print "Total number of CUTS at cystectomy was: ", cut_cystectomies
print "Total number of included pathologies was: ", path_included
print "Total number of CUTS at pathology was: ", cut_pathology
print "Total number included at cancer sequence was: ", sequence_included
print "Total number of CUTS at cancer sequence was: ", sequence_cut

