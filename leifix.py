#!/usr/local/bin/python

import re
import csv
from geopy import geocoders

#Make a dictionary using a csv file
def dictmaker(reference, column1, column2):
	sourcefile = open(reference,'rb')
	sourcereader=csv.reader(sourcefile)

	dictionary = {}

	for srow in sourcereader:
		if srow[column1] != "" and srow[column2] != "" and srow[column2] != "N/A" and srow[column2] != "#N/A":
			dictionary[srow[column1]] = srow[column2]
	sourcefile.close()

	return dictionary

#Encoding fixer function
def encodingfix(phrase, listlocation, finalencoding):
	#print phrase
	newphrase = ''
	for l in phrase:
		encodefile = open(listlocation, 'r')
		encodelist = eval(encodefile.read())
		for encoding in encodelist:
			try:
				l = l.decode(encoding)			
				break
			except:
				pass
		newphrase = newphrase + l
		encodefile.close()
	return newphrase

#Country code fixer function
def countryfix(text, dictlocation):
	dictfile = open(dictlocation, 'r')
	dictionary = eval(dictfile.read())

	pattern = re.compile(r'\b(' + '|'.join(dictionary.keys()) + r')\b')	
	try:
		result = pattern.sub(lambda x: dictionary[x.group()], text)
		return result
		#print text
	except:
		return text
	dictfile.close()

#Check for previously geocoded LEIs
def lookup(lei, latdict, longdict):
	try:
		latitude = latdict[lei]
		longitude = longdict[lei]
		coordinates = [latitude, longitude]
		return coordinates
	except:
		raise Exception("Not in dictionary.")

#Geocoding function (requires keeping track of bing and yahoo counts outside of function)
def geocoder(address, bingcount, yahoocount):
	b0 = geocoders.Bing('AqEiMxH7LImOr8FH5V8JhUpuRIY52bsNPnNS5S_8P-dceYBCK73OIKUC_DoBmA1o')
	b1 = geocoders.Bing('AviHPHHl3c3QnLdMwsNvJV3te3P7krJ_YqJbhhHuqz-ejQulFTL1SmmqPNB3cuHu')
	b2 = geocoders.Bing('ApotMrYSsjzheNRWMYcmIPd1MwPoFmCSjTEYzb3EkV8iAljoGbCV_T7YylnRSSWo')
	b3 = geocoders.Bing('AjhNYowwfCMG88V_AC-lUh1kF1WMVJwwSBiUPmtIVrZvXDaLWGQ7__d4R5_rRjm_')
	y0 = geocoders.YahooPlaceFinder('dj0yJmk9QmN3cUNVNDQ3YWhLJmQ9WVdrOVUxaFpSMlpOTmpJbWNHbzlNVFV6TURJM05EWXkmcz1jb25zdW1lcnNlY3JldCZ4PWNm', 'c985e466b543c2b2e723ea3c62c03a7919725f6c')
	y1 = geocoders.YahooPlaceFinder('dj0yJmk9RHB4WHZ3STRXTXJzJmQ9WVdrOWNITlhUM0ZoTjJjbWNHbzlOREl4TnpVNE16WXkmcz1jb25zdW1lcnNlY3JldCZ4PTA1', '86c31a3fbdbec62f26521bbc21ccf3da109edd3d')
	g = geocoders.GoogleV3()
	b = [b0,b1,b2,b3]
	y = [y0,y1]
		
	#Attempt to find gps coordinates and add them to their respective elements	
	try:
		place, (lat, lng) = b[bingcount].geocode(address)
		bingcount = bingcount + 1
		latitude = str(lat)
		longitude = str(lng)
	except:
		try:
			bingcount = bingcount + 1
			place, (lat, lng) = y[yahoocount].geocode(address)
			yahoocount = yahoocount + 1
			latitude = str(lat)
			longitude = str(lng)
		except:
			try:
				yahoocount = yahoocount + 1
				place, (lat, lng) = g.geocode(address)
				latitude = str(lat)
				longitude = str(lng)
			except:
				latitude = "N/A"
				longitude = "N/A"

	if bingcount == 4:
		bingcount = 0
	if yahoocount == 2:
		yahoocount = 0

	coordinates = [latitude, longitude, bingcount, yahoocount]
	return coordinates