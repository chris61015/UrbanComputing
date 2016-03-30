#encoding=utf-8
import os
import xml.dom.minidom
import csv
import geojson

"""
South: lat=40.477399
North: lat=40.917577
West: lon=-74.25909
Eest: lon=-73.7001716
"""

def isInNYC(lon, lat):
	if  (-74.25909 <= lon and lon <= -73.7001716) and (40.477399 <= lat and lat <= 40.917577):
		return True
	else:
		return False

def writeFile(fileName,row):
	newFileName = ''
	if 'NYC_' not in fileName:
		newFileName = 'NYC_%s' % fileName
	else: 
		newFileName = fileName
	outPut = open(newFileName, 'w')
	outPut.writelines(row)

def genGeoJson(fileName, s):
	print fileName
	outPutName = ''
	if 'PM2.5' in fileName:
		outPutName = 'PM2_5.geojson'
	elif 'PM10' in fileName:
		outPutName = 'PM10.geojson'
	else :	
		outPutName = 'default.geojson'

	newList = [(float(k),float(v)) for (k,v) in s]
	geoData = geojson.MultiPoint(list(newList))
	geoJson = geojson.Feature(geometry=geoData, properties={"Sites": outPutName.split('.')[0]})
	
	outPut = open(outPutName, 'w')
	geojson.dump(geoJson, outPut)

def main():
	path = os.getcwd()
	for fileName in os.listdir(path):
		print fileName
		if '.csv' not in fileName or 'NYC_' in fileName:
			continue
		f = open(fileName).readlines()
		row = [f[0]]
		s = set()
		for line in f:
			temp = line.split(',')
			if "New York" in line and isInNYC(float(temp[6]), float(temp[5])):
				row.append(line)
				s.add((temp[6],temp[5]))
		if row:		
			writeFile(fileName,row)
		if s:
			genGeoJson(fileName, s)

if __name__ == '__main__':
	main();