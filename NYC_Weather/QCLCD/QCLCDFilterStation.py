#encoding=utf8
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

def genGeoJson(fileName, s):

	geoData = geojson.MultiPoint(s)
	geoJson = geojson.Feature(geometry=geoData, properties={"Sites": fileName.split('.')[0]})
	
	with open(fileName, 'w') as outPut:
		geojson.dump(geoJson, outPut)

if __name__ == '__main__':
	content = []
	with open('201510station.txt') as f:
		next(f)
		for line in f:
			data = line.split('|')
			if  'NY' in data[7] and isInNYC(float(data[-5]), float(data[-6])):
				content.append((float(data[-5]), float(data[-6])))

	genGeoJson('obs.geojson',content)
	# output = open('NY_Station.txt', 'w')
	# output.writelines(content)			
