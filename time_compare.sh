#!/bin/bash -x

# 0. read sites.txt 
# Each line is site address. 
# if it contains "cdn" then it is page for AMP

# nytimes
# https://mobile-nytimes-com.cdn.ampproject.org/c/s/mobile.nytimes.com/2017/05/27/opinion/sunday/defenders-of-the-faith-in-government.amp.html
# https://mobile.nytimes.com/2017/05/27/opinion/sunday/defenders-of-the-faith-in-government.html
# searchengineland 
# http://searchengineland.com/adwords-maximize-conversions-smart-bidding-276064
# https://searchengineland-com.cdn.ampproject.org/c/searchengineland.com/adwords-maximize-conversions-smart-bidding-276064/amp
SITE="sites_170627.txt"
echo "" > visit.sh
i=0
while read line
do
# 1. Install the application
	site=$line
	prefix0="https://mobile-nytimes-com.cdn.ampproject.org/c/s/mobile.nytimes.com/"
	prefix1="https://mobile.nytimes.com/"
	prefix2="http://searchengineland.com/"
	prefix3="https://searchengineland-com.cdn.ampproject.org/c/searchengineland.com/"

	logfile=${line#${prefix0}}
	logfile=${logfile#${prefix1}}
	logfile=${logfile#${prefix2}}
	logfile=${logfile#${prefix3}}
	logfile=`echo $logfile | sed -e 's/\//_/g'`
	logfile="../logs/$logfile"

	echo "./bash.sh $site $logfile" >> visit.sh
#	i=`expr $i + 1`
#	reboot=`expr $i % 10`
#	if [ $reboot -eq 0 ]; then
#		echo "adb reboot" >> visit.sh
#		echo "sleep 40" >> visit.sh
#	fi


done < $SITE

cp visit.sh page_speed/visit.sh
cd page_speed
./visit.sh
