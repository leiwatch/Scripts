#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import shutil

rfile = open(sys.argv[1]+'Data/Final.csv','rb')
reader=csv.reader(rfile)
ofile = open(sys.argv[1]+'Data/temp.csv','wb')
writer=csv.writer(ofile)

changecounter=0

for row in reader:
	if row[13] == 'London Stock Exchange' or row[13] == 'Dutch Chamber of Commerce':
		if row[11].startswith('201'):
			pass
		else:
			changecounter=changecounter+1
			if '-' in row[11]:
				day = row[11][0:2]
				month = row[11][3:5]
				year = row[11][6:]
				new = year + '-' + month + '-' + day
				row[11] = new
			elif '/' in row[11]:
				day = row[11][:row[11].find('/')]
			
				counter = 0
				for d in day:
					counter = counter + 1	
				month = row[11][row[11].find(day)+counter+1:row[11].find('201')-1]
				temp = row[11][:row[11].find('201')-1]
				if counter < 2:
					day = '0' + day	
				
				tempcounter = 0
				for d in temp:
					tempcounter = tempcounter + 1			
				year = row[11][row[11].find(temp)+tempcounter+1:]
				
				counter = 0
				for d in month:
					counter = counter + 1	
				if counter < 2:
					month = '0' + month
					
				new = year + '-' + month + '-' + day
				row[11] = new
			else:
				pass
		if row[12].startswith('201'):
			pass
		else:
			if '-' in row[12]:
				day = row[12][0:2]
				month = row[12][3:5]
				year = row[12][6:]
				new = year + '-' + month + '-' + day
				row[12] = new
			elif '/' in row[12]:
				#print row[12]
				day = row[12][:row[12].find('/')]
			
				counter = 0
				for d in day:
					counter = counter + 1	
				month = row[12][row[12].find(day)+counter+1:row[12].find('201')-1]
				temp = row[12][:row[12].find('201')-1]
				if counter < 2:
					day = '0' + day	
				
				tempcounter = 0
				for d in temp:
					tempcounter = tempcounter + 1			
				year = row[12][row[12].find(temp)+tempcounter+1:]
				
				counter = 0
				for d in month:
					counter = counter + 1	
				if counter < 2:
					month = '0' + month
					
				new = year + '-' + month + '-' + day
				row[12] = new
			else:
				pass
	else:
		if 'T' in row[11]:
			changecounter=changecounter+1
			new = row[11][:row[11].find('T')]
			row[11] = new
		else:
			pass
		if 'T' in row[12]:	
			new = row[12][:row[12].find('T')]
			row[12] = new
		else:
			pass

	writer.writerow(row)

print 'Number of rows changed: ' + str(changecounter)

rfile.close()
ofile.close()
shutil.copy2(sys.argv[1]+'Data/temp.csv', sys.argv[1]+'Data/temp.csv')
