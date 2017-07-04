import os
import collections

#dicM={} #Mobile DOMLoad
#dicA={} #AMP DOMLoad
#os.system("grep -Rn \"\\\"DOMLoad\"\\\" logs/* > DOMLoad.txt")
#f = open("DOMLoad.txt")
#lines = f.readlines()
#
#for line in lines:
#	site = line.split(":")[0].split("/")[1]
#	DOMLoad = line.split("{")[1].split(":")[1].split("}")[0]
#	
#	if site.find("amp") > 0:
#		dicA[site] = DOMLoad
#	else:
#		dicM[site] = DOMLoad
#
#print("Mobile = ",len(dicM)," AMPages = ",len(dicA))
#print("seq\tsites\tmobile\tAMPage\tMobile-AMPage")
#seq=0
#for mobile in dicM.keys():
#	AMPage = mobile+"_amp"
#	if AMPage in dicA.keys():
#		print("{0}\t{1}\t{2}\t{3}\t{4}".format(seq, mobile, float(dicM[mobile]), float(dicA[AMPage]), float(dicM[mobile])-float(dicA[AMPage])))
#		seq=seq+1

#dicMN={} #mobile Download
#dicAN={}
#fn = open ("time_download.txt")
#lines = fn.readlines()
#for line in lines:
#	site = line.split("/")[4].split("^")[0]
#	netw = line.split(":")[3].split("\n")[0]
#
#	if site.endswith("amp") > 0:
#		site = site.split("c_")[1]
#		dicAN[site] = netw
#	else:
#		dicMN[site] = netw
#	
#
#dicMB={} #mobile Bytes
#dicAB={}
#fb = open ("num_bytes_all.txt")
#lines = fb.readlines()
#for line in lines:
#	site = line.split("/")[4].split("^")[0]
#	byte = line.split(":")[3].split("\n")[0]
#
#	if site.endswith("amp") > 0:
#		site = site.split("c_")[1]
#		dicAB[site] = byte
#	else:
#		dicMB[site] = byte
#	
#
#dicMC={}
#dicAC={}
#fc = open ("time_comp.txt")
#lines = fc.readlines()
#for line in lines:
#	site = line.split("/")[4].split("^")[0]
#	comp = line.split(":")[3].split("\n")[0]
#
#	if site.endswith("amp") > 0:
#		site = site.split("c_")[1]
#		dicAC[site] = comp
#	else:
#		dicMC[site] = comp

#os.system("grep -Rn \"\\<load:\" tests/analysis_t/temp_files/ALL_pro/* | grep 'ALL_pro/searchengineland' > load.txt");
#os.system("grep -Rn \"\\<time_comp:\" tests/analysis_t/temp_files/ALL_pro/* | grep 'ALL_pro/searchengineland' > time_comp.txt");
#os.system("grep -Rn \"\\<num_bytes_all:\" tests/analysis_t/temp_files/ALL_pro/* | grep 'ALL_pro/searchengineland' > num_bytes_all.txt");
#os.system("grep -Rn \"\\<time_download:\" tests/analysis_t/temp_files/ALL_pro/* | grep 'ALL_pro/searchengineland' > time_download.txt");

os.system("egrep -Rn '^load|^HTMLParse|^time_download|^time_comp|^time_block|^dep|^time_block_js|^num_domains_cp|^num_bytes_all|' tests/analysis_t/temp_files/ALL_pro/* | grep 'ALL_pro/searchengineland' > extract.txt");

dicM=collections.OrderedDict() 
dicA=collections.OrderedDict() 
f = open ("extract.txt")
lines = f.readlines()
index = 0
global load, HTMLParse, time_download, time_comp, time_block, dep_D2E, dep_E2D_html, dep_E2D_css, dep_E2D_js, dep_RFB, dep_HOL_css, dep_HOL_js, time_block_js, num_domains_cp, num_bytes_all, PostParse
switch_case = {
	"load" : 0,
	"HTMLParse" : 1,
	"PostParse" : 2,
	"time_download" : 3,
	"time_comp" : 4,
	"time_block" : 5,
	"dep_D2E" : 6,
	"dep_E2D_html" : 7,
	"dep_E2D_css" : 8,
	"dep_E2D_js" : 9,
	"dep_RFB" : 10,
	"dep_HOL_css" : 11,
	"dep_HOL_js" : 12,
	"time_block_js" : 13,
	"num_domains_cp" : 14,
	"num_bytes_all" : 15,
}
for line in lines:
	site = line.split("/")[4].split("^")[0]
	value = line.split(":")[2]
	time = line.split(":")[3].split("\n")[0]

	if site.endswith("amp") > 0:
		site = site.split("c_")[1]
		dicA[site+"@"+value] = time
	else:
		dicM[site+"@"+value] = time

seq=0
print(str(len(dicA)) + " " + str(len(dicM)))
fw = open("Mobile_AMP_Result.txt", "w")
fw.write("site load A HTMLParse A PostParse A download A comp A block A dep_D2E A dep_E2D_html A dep_E2D_css A dep_E2D_js A dep_RFB A dep_HOL_css A dep_HOL_js A block_js A domain_cp A bytes A\n")
string = ""
prev_site = ""
write = True
for siteAtValue in dicM.keys():
	site = siteAtValue.split("@")[0]
	value = siteAtValue.split("@")[1]

	if prev_site != site:
		if len(string) > len(site)+50 and write == True :
			fw.write(string + "\n")
		prev_site = site
		string = site + " "
		write = True
	
	try:
		result = switch_case[value]
	except KeyError:
		continue
		
	AMPage = site+"_amp"
	if AMPage+"@"+value in dicA.keys():
		if value == "time_download" or value == "time_comp" or value == "time_block" or value == "time_block_js" or value == "PostParse":
			string = string + str(float(dicM[siteAtValue])/1000) + " " + str(float(dicA[AMPage+"@"+value])/1000) + " "
			if float(dicM[siteAtValue]) < 0 or float(dicA[AMPage+"@"+value]) < 0:
				write = False
		else:
			string = string + dicM[siteAtValue] + " " + dicA[AMPage+"@"+value] + " " 
	



#fw.write(mobile + "\t" + dicML[mobile] + "\t" + str(float(dicMC[mobile])/1000) + "\t" + str(float(dicMN[mobile])/1000) + "\t" + dicMB[mobile] + "\t" + dicAL[AMPage]+ "\t"  + str(float(dicAC[AMPage])/1000)+ "\t" + str(float(dicAN[AMPage])/1000) + "\t" + dicAB[AMPage] + "\t" + str(float(dicML[mobile])/float(dicAL[AMPage])) + "\n")

#print(site + " " + load)

#	try:
#		result = switch_case[value]
#	except KeyError:
#		result = 0
#
#	if result == 0:
#		load = time
#	elif result == 1:
#		HTMLParse = time
#	elif result == 2:
#		download = time
#	elif result == 3:
#		comp = time
#	elif result == 4:
#		block = time
#	elif result == 5:
#		dep_D2E = time
#	elif result == 6:
#		dep_E2D_html = time
#	elif result == 7:
#		dep_E2D_css = time
#	elif result == 8:
#		dep_E2D_js = time
#	elif result == 9:
#		dep_RFB = time
#	elif result == 10:
#		dep_HOL_css = time
#	elif result == 11:
#		dep_HOL_js = time
#	elif result == 12:
#		time_block_js = time
#	elif result == 13:
#		num_domains_cp = time
#	elif result == 14:
#		num_bytes_all = time
