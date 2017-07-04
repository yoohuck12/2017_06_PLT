import os
import sys

HomeF="/home/linuxhyuck"

#site generation - executing crawler
#Download web pages in beatifulF/webpages
beatifulF=HomeF+"/Research/web_crawler/beautifulSoup"
os.system('python '+beatifulF+'/mobile_nytimes.py') #This file saves html file with beautifulSoap but I (maybe) replace it with wget to download files/images.

#python for making sites.txt
os.system('python '+beatifulF+'/webpages/extract_sites.py')

#read sites and execute it with Colin's bash.rc
ColinF=HomeF+"/Research/Colin"
os.system('python read_sites_and_executes.py')

