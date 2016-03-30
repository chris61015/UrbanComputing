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

def writeFile(filePath, fileName,row):
	newFileName = ''
	if 'NYC_' not in fileName:
		newFileName = 'NYC_%s' % fileName
	else: 
		newFileName = fileName
	
	outPut = open(os.path.join(filePath, newFileName), 'w')
	outPut.writelines(row)


def genGpx(fileName,s):
	gpxDoc = xml.dom.minidom.Document()
  
	gpxElement = gpxDoc.createElementNS('http://www.topografix.com/GPX/1/1', 'gpx')
	gpxElement.setAttribute('xmlns','http://www.topografix.com/GPX/1/1')
	gpxElement.setAttribute('version','1.1')
	gpxElement.setAttribute('creator','TrackConverter')
	gpxElement = gpxDoc.appendChild(gpxElement)

  	for tup in s:
		# wptElement = genWpt(gpxDoc,tup)
		wptElement = gpxDoc.createElement('wpt')
		wptElement = gpxElement.appendChild(wptElement) 
		wptElement.setAttribute('lat', tup[0])
		wptElement.setAttribute('lon', tup[1])
    	

  	gpxFileName = '%s.gpx'	% fileName.split('.')[0]
  	gpxFile = open(gpxFileName, 'w')
  	gpxFile.write(gpxDoc.toprettyxml(indent='  ', newl = '\n', encoding = 'utf-8'))

def genGeoJson(filePath,fileName, s):

	outPutName = ''
	if 'PRESS' in fileName:
		outPutName = 'barometer.geojson'
	elif 'RH_DP' in fileName:
		outPutName = 'hygrometer.geojson'
	elif 'TEMP' in fileName:
		outPutName = 'thermometer.geojson'
	elif 'WIND' in fileName: 
		outPutName = 'anemometer.geojson'
	else :	
		outPutName = 'default.geojson'

	newList = [(float(k),float(v)) for (k,v) in s]
	geoData = geojson.MultiPoint(list(newList))
	geoJson = geojson.Feature(geometry=geoData, properties={"Sites": outPutName.split('.')[0]})
	
	outPut = open(os.path.join(filePath,outPutName), 'w')
	geojson.dump(geoJson, outPut)

def main():
	filePath = os.path.join(os.getcwd(),'AQS_Data')
	for fileName in os.listdir(filePath):
		if '.csv' not in fileName or 'NYC_' in fileName:
			continue
		f = open(os.path.join(filePath,fileName)).readlines()
		row = [f[0]]
		s = set()
		for line in f:
			temp = line.split(',')
			if "New York" in line and isInNYC(float(temp[6]), float(temp[5])):
				row.append(line)
				s.add((temp[6],temp[5]))
		if row:		
			writeFile(filePath, fileName,row)
		# if s: 
		# 	genGpx(fileName, s)
		if s:
			genGeoJson(filePath, fileName, s)

if __name__ == '__main__':
	main();