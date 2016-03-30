#encoding=utf8
import geojson
import ast
import datetime
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

def inTime(time):
	t = datetime.datetime.strptime(time, '%Y%m%d')
	cprt =  datetime.datetime.strptime('20150630', '%Y%m%d')
	return t >= cprt
if __name__ == '__main__':
	content = []
	with open('station.csv') as f:
		next(f)
		for line in f:
			data = line.split(',')
			
			lon = ast.literal_eval(data[7])
			lat = ast.literal_eval(data[6])
			if  lon!="" and lat!="":
				flon, flat = float(lon), float(lat)
				if eval(data[4])=='NY' and isInNYC(flon, flat) and inTime(data[-1].strip('"\n')):
					content.append((flon, flat))
					# content.append(line)

	genGeoJson('GSOD_obs.geojson',content)
	# output = open('NY_Station.txt', 'w')
	# output.writelines(content)			
