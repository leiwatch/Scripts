#!/bin/bash

FOLDER="/Users/user/Documents/Sync/CIFER Lab/test/"
#LOUS=("GMEI" "GEI" "IEI" "INSEE" "ISE" "KVK" "Takas")
LOUS=("GMEI" "GEI" "IEI" "INSEE" "ISE" "KVK")

echo "LEI Updater - "$(date +%Y%m%d) > "$FOLDER""Logs/""$(date +%Y%m%d)"".log"
for LOU in "${LOUS[@]}"
do
	NEWLOU=false
	echo $LOU >> "$FOLDER""Logs/""$(date +%Y%m%d)"".log"
	#
	#Check if LOU logfile exists and create one if not
	if [ ! -f "$FOLDER""LOUs/""$LOU""/""$LOU".log ]
	then	
		echo "Creating "$LOU" logfile..." >> "$FOLDER""Logs/""$(date +%Y%m%d)"".log"
		touch "$FOLDER""LOUs/""$LOU""/""$LOU".log
	fi
	
	#Get LOU last update date
	LASTDATE=$(<"$FOLDER""LOUs/""$LOU""/""$LOU".log)

	#Check if date in logfile exists, if not turn boolean on for use in downloading a full file
	if [ "$LASTDATE" == "" ]
	then
		NEWLOU=true
	fi
	
	#Update files until they reach the current date
	while [[ "$LASTDATE" < $(date +%Y%m%d) ]]
	do
		if [ "$NEWLOU" = true ]
		then
			YEAR=$(date +%Y)
			MONTH=$(date +%m)
			DAY=$(date +%d)
		else
			YEAR=$(date -j -v+1d -f "%Y%m%d" $LASTDATE +%Y)
			MONTH=$(date -j -v+1d -f "%Y%m%d" $LASTDATE +%m)
			DAY=$(date -j -v+1d -f "%Y%m%d" $LASTDATE +%d)
		fi

		echo "Looking up $LOU data for $YEAR$MONTH$DAY..." >> "$FOLDER""Logs/""$(date +%Y%m%d)"".log"
		python "$FOLDER""LOUs/""$LOU""/""$LOU"".py" "$FOLDER" $YEAR$MONTH$DAY $NEWLOU >> "$FOLDER""Logs/""$(date +%Y%m%d)"".log"

		#if [ "$NEWLOU" = true ]
		#then
		#	python "$FOLDER""Scripts/leilookup.py" "$FOLDER" >> "$FOLDER""Logs/""$(date +%Y%m%d)"".log"
		#fi
		#python "$FOLDER""Scripts/geocoder.py" "$FOLDER" "PreFinal" >> "$FOLDER""Logs/""$(date +%Y%m%d)"".log"
		
		#In case there are problems where the python script does not update its log, causing a loop,
		#the following will test for if $LASTDATE is updated and escape the while loop if it is not.
		COMPAREDATE="$LASTDATE"
		LASTDATE=$(<"$FOLDER""LOUs/""$LOU""/""$LOU".log)
		if [[ "$LASTDATE" == "$COMPAREDATE" ]]
		then
			LASTDATE=$(date +%Y%m%d)
		else
			/Applications/Pentaho/pan.sh -file="$FOLDER""LOUs/""$LOU""/""$LOU"".ktr" -level=Minimal >> "$FOLDER""Logs/""$(date +%Y%m%d)"".log"
		fi
	done
done

if [ "$DAY" == "01" ]
then
	python "$FOLDER""Scripts/geocoder.py" "$FOLDER" "Final" >> "$FOLDER""Logs/""$(date +%Y%m%d)"".log"
fi
python "$FOLDER""Scripts/datefixer.py" "$FOLDER" >> "$FOLDER""Logs/""$(date +%Y%m%d)"".log"
