#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import shutil
from geopy import geocoders

ifile = open(sys.argv[1]+'Data/'+sys.argv[2]+'.csv','rb')
reader=csv.reader(ifile)
ofile = open(sys.argv[1]+'Data/temp.csv','wb')
writer = csv.writer(ofile, delimiter=',', quotechar='"')

b0 = geocoders.Bing('AqEiMxH7LImOr8FH5V8JhUpuRIY52bsNPnNS5S_8P-dceYBCK73OIKUC_DoBmA1o')
b1 = geocoders.Bing('AviHPHHl3c3QnLdMwsNvJV3te3P7krJ_YqJbhhHuqz-ejQulFTL1SmmqPNB3cuHu')
b2 = geocoders.Bing('ApotMrYSsjzheNRWMYcmIPd1MwPoFmCSjTEYzb3EkV8iAljoGbCV_T7YylnRSSWo')
b3 = geocoders.Bing('AjhNYowwfCMG88V_AC-lUh1kF1WMVJwwSBiUPmtIVrZvXDaLWGQ7__d4R5_rRjm_')
y0 = geocoders.YahooPlaceFinder('dj0yJmk9QmN3cUNVNDQ3YWhLJmQ9WVdrOVUxaFpSMlpOTmpJbWNHbzlNVFV6TURJM05EWXkmcz1jb25zdW1lcnNlY3JldCZ4PWNm', 'c985e466b543c2b2e723ea3c62c03a7919725f6c')
y1 = geocoders.YahooPlaceFinder('dj0yJmk9RHB4WHZ3STRXTXJzJmQ9WVdrOWNITlhUM0ZoTjJjbWNHbzlOREl4TnpVNE16WXkmcz1jb25zdW1lcnNlY3JldCZ4PTA1', '86c31a3fbdbec62f26521bbc21ccf3da109edd3d')
g = geocoders.GoogleV3()
b = [b0,b1,b2,b3]
y = [y0,y1]
bingcount = 0
yahoocount = 0

geoattempts = 0
geoerror = 0

for row in reader:
	if row[9] == "" or row[9] == "N/A" or row[9] == "#N/A":
		geoattempts = geoattempts + 1
		addrs = row[8]
		
		#Attempt to find gps coordinates and add them to their respective elements	
		try:
			place, (lat, lng) = b[bingcount].geocode(addrs)
			row[9] = str(lat)
			row[10] = str(lng)
			#print "Latitude: " + str(lat)
			#print "Longitude: " + str(lng)
			bingcount = bingcount + 1
		except:
			try:
				place, (lat, lng) = y[yahoocount].geocode(addrs)
				row[9] = str(lat)
				row[10] = str(lng)
				#print "Latitude: " + str(lat)
				#print "Longitude: " + str(lng)
				yahoocount = yahoocount + 1
			except:
				try:
					place, (lat, lng) = g.geocode(addrs)
					row[9] = str(lat)
					row[10] = str(lng)
					#print "Latitude: " + str(lat)
					#print "Longitude: " + str(lng)
				except:
					#print "Error..."
					row[9] = "N/A"
					row[10] = "N/A"
					geoerror = geoerror + 1
	
		if bingcount == 4:
			bingcount = 0
		if yahoocount == 2:
			yahoocount = 0
	else:			
		pass

	writer.writerow(row)

print "Number of Geocoding Attempts: " + str(geoattempts)
print "Number of Geocoding Errors: " + str(geoerror)	
	
ifile.close()
ofile.close()
shutil.copy2(sys.argv[1]+'Data/temp.csv', sys.argv[1]+'Data/'+sys.argv[2]+'.csv')
