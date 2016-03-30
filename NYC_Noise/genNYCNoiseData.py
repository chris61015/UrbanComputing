#encoding=utf-8
import os
import geojson
import datetime
import ast
import pandas as pd
import numpy as np
from dateutil import rrule
import sys
"""
South: lat=40.477399
North: lat=40.917577
West: lon=-74.25909
Eest: lon=-73.7001716
"""
lst = []
def printx(x):
	lst.append(x)
def countEventInTime(st, et, timeList):
	# run rrule for add one month to st on every loop until it reachs et
	tSpanList = []
	for date in rrule.rrule(rrule.HOURLY, dtstart=st, until=et):
		tSpanList.append(date)

	df = pd.DataFrame([1]*len(timeList),index=timeList, columns=['Count'])
	s = df.groupby(pd.TimeGrouper(freq='H')).count().as_matrix()

 	pairs = []
 	for index in range(len(s)):
 		pairs.append({tSpanList[index] + datetime.timedelta(hours=1) :s[index][0]})
 	print pairs
 	line = ''
 	for index in range(len(pairs)):
 		if (index % 24 == 0):
 			line += "\n"
 		line += str(pairs[index].values())
 	print line
	# for index in range(len(rtnList)):
	# 	if index+1 < len(rtnList):
	# 		st = rtnList[index]
	# 		et = rtnList[index + 1]
	# 		print st, et
	# 		print df.between_time(st,et)
	# 		print '----------------------'

	# s = df.groupby(pd.TimeGrouper(freq='H')).count().get_values()
 	# print type(s), s
	
def timeConverter(time, Tformat):
	return datetime.datetime.strptime(time,Tformat)

def withInTime(st, et, dt):
	if (st <= dt) and (dt < et):
		return True
	else:
		return False

def writeFile(fileName,row):
	outPut = open(fileName, 'w')
	outPut.writelines(row)

def genGeoJson(fileName, s):

	# newList = [(float(k),float(v)) for (k,v) in s]
	geoData = geojson.MultiPoint(list(s))
	geoJson = geojson.Feature(geometry=geoData, properties={"Sites": fileName.split('.')[0]})
	
	outPut = open(fileName, 'w')
	geojson.dump(geoJson, outPut)

def main():
	with open('311_Service_Requests_from_2010_to_Present.csv') as f:
		lines = f.readlines()
		row = [lines[0]]
		startTime = timeConverter('2014/07/01','%Y/%m/%d')
		endTime = timeConverter('2015/07/01','%Y/%m/%d')
		timeList = []
		s = set()
		for line in lines[1:]:
			temp = line.split(',')
			dataTime =  timeConverter(temp[1],'%m/%d/%Y %I:%M:%S %p')
			if withInTime(startTime, endTime, dataTime):
				row.append(line)
				timeList.append(dataTime)

				if (temp[-3]!='' and temp[-4]!=''):
					s.add((float(temp[-3]),float(temp[-4])))

		countEventInTime(startTime, endTime, timeList)

		if row:		
			writeFile('NYC_NoiseData.csv',row)
		if s:
			genGeoJson('Noise.geojson', s)

if __name__ == '__main__':
	main();