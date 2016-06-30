#encoding=utf-8
import os
import xml.dom.minidom
import csv
import geojson

def genGeoJson(fileName, s):

	geoData = geojson.MultiPoint(s)
	geoJson = geojson.Feature(geometry=geoData, properties={"Sites": fileName.split('.')[0]})
	
	outPut = open(fileName, 'w')
	geojson.dump(geoJson, outPut)

def main():
	coordinates = []
	curPath = os.getcwd()
	filePath = os.path.join(curPath, 'RawData','new york_anon_locationData_newcrawl.txt')
	with open(filePath) as f:
		content = f.readlines()
		for line in content:
			data = line.split(';')[1].strip('*\n()').split(',')

			coordinates.append((float(data[1]),float(data[0])))
	genGeoJson('POI.geojson',coordinates)		


if __name__ == '__main__':
	main();