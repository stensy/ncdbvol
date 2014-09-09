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

cystlist = []
included_path_t = []
included_path_n = []
histlist = []

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

			## Only include transitional cell carcinoma
			if row[18] in histlist:
				histology_included += 1
			else:
				histology_cut += 1
				continue

			## Only included cases with NO radiation
			if row[41] == '0':
				radiation_included += 1
			else:
				radiation_cut += 1
				continue
			
			## Only include cases if patient survived 30 days
			if row[46] == '0':
				mortality_included += 1
			else:
				mortality_cut += 1
				continue

			## Only include cases if patient received NO or ADJUVANT chemo
			if row[45] == '0':
				adjuvantchemo = 0
				chemo_included += 1
				no_chemo += 1
			elif row[45] == '3':
				adjuvantchemo = 1
				chemo_included += 1
				got_chemo += 1
			else:
				chemo_cut += 1
				continue

			## Only include chemo cases that received chemo within 90 days of surgery.
			if row[45] == '3':
				try:
					days_post_surg = int(row[49])
				except:
					days_post_surg = 9999
					missing_post_surg_timing += 1

				if days_post_surg <=90:
					adjuvant_included += 1
				else:
					adjuvant_cut += 1
					continue
			else:
				no_chemo_2 += 1
				adjuvant_included += 1

			included_cases += 1
			ncdbout.writerow(row)

print "Total number of cases was: ", totalcases
print "Total number of cystectomies was: ", cystectomies
print "Total number of CUTS at cystectomy was: ", cut_cystectomies
print "Total number of included pathologies was: ", path_included
print "Total number of CUTS at pathology was: ", cut_pathology
print "Total number included at cancer sequence was: ", sequence_included
print "Total number of CUTS at cancer sequence was: ", sequence_cut
print "Total number included for TCC was: ", histology_included
print "Total number of CUTS at histology was: ", histology_cut
print "Total number included for no radiation was: ", radiation_included
print "Total number of CUTS at radiation was: ", radiation_cut
print "Total number included for mortality was: ", mortality_included
print "Total number of CUTS at mortality was: ", mortality_cut
print "Total number included for chemo was: ", chemo_included
print "Total number of CUTS at chemo was: ", chemo_cut
print "Number of patients receiving chemo after cystectomy was: ", got_chemo
print "Number of patients NOT receiving chemo after cystectomy was: ", no_chemo
print "Total number of patients included after adjuvant cut was: ", adjuvant_included
print "Total number of CUTS for adjuvant chemo timing was: ", adjuvant_cut
print "For consistency, patients NOT receiving chemo after cystectomy was: ", no_chemo_2
print "Final number of included cases was: ", included_cases
print "Number of missing post surg timing values was: ", missing_post_surg_timing
print "Total cases was %i, computed cases from cuts and included cases is %i." % (totalcases, included_cases + cut_cystectomies + cut_pathology + sequence_cut + histology_cut + radiation_cut + mortality_cut + chemo_cut + adjuvant_cut)

