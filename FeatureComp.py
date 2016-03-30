#-*- coding: utf-8 -*-
import math
import os
import copy
import geojson
import math
import csv
import datetime
import numpy as np
from scipy import special, optimize

# Do not include Staten Island in the NYC
latMin = 40.542981
latMax = 40.917577
lonMin = -74.041994
lonMax = -73.7001716    
gridLength = 1000
gridWidth = 1000

def rad(d):
    return d*math.pi/180.0

#Calculate the distance between two coordinates in meters
def distance(lat1,lng1,lat2,lng2):
    radlat1=rad(lat1)
    radlat2=rad(lat2)
    a=radlat1-radlat2
    b=rad(lng1)-rad(lng2)
    s=2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))
    earth_radius=6378.137
    s=s*earth_radius
    return s * 1000

#calculate how many rows and columns are there in our grid.
def numOfGrid():
  lonRange = distance( latMin,  lonMin,  latMin,  lonMax)
  latRange = distance( latMin,  lonMin,  latMax,  lonMin)
  return  int((latRange // gridWidth) +1), int((lonRange // gridLength) + 1)

#turn GPS coordinate into Grid ID
def gridCoor(mlist, lat, lon, m, n, cnt):
  
    col = int(distance(latMax,lon,latMax,lonMin) / gridLength)
    row = int(distance(lat,lonMin,latMax,lonMin) / gridWidth)
    if (row>= 0 and row<m and col>=0 and col<n):
      mlist[row][col]+=cnt
    # print 'id:%d' % (row * len(r) + col + 1)

#turn GPS coordinate into Grid ID
def gridCoorCate(cateList, cate, lat, lon, m, n):
    
    col = int(distance(latMax,lon,latMax,lonMin) / gridLength)
    row = int(distance(lat,lonMin,latMax,lonMin) / gridWidth)
    if (row>= 0 and row<m and col>=0 and col<n):
      cateList[row][col][cate] += 1
    # print 'id:%d' % (row * len(r) + col + 1)

def getBikeDensity(curPath, m, n):
    mlist = [[0 for col in range(n)] for row in range(m)] #initialize the matrix to 0
    geoJsonFile = os.path.join(curPath, 'NYC_Bike', 'bike.geojson')
    with open(geoJsonFile) as f:
        data = geojson.load(f)
        for coor in data['geometry']['coordinates']:
            gridCoor(mlist, coor[1], coor[0], m, n, 1)
    return mlist    

def getPOIDensity(curPath, m, n):
    mlist = [[0 for col in range(n)] for row in range(m)] #initialize the matrix to 0
    filePath = os.path.join(curPath, 'NYC_POI', 'RawData', 'new york_anon_locationData_newcrawl.txt')
    with open(filePath) as f:
        lines = f.readlines()
        for line in lines:
            data = line.split(';')[1].strip('()*').split(',')
            lat = float(data[0])
            lon = float(data[1])
            gridCoor(mlist, lat, lon, m, n, 1)

    return mlist  

def calEntropy(cateList, m, n):
    rtnlist = [[0 for col in range(n)] for row in range(m)] #initialize the matrix to 0
    for i in range(m):
        for j in range(n):
            total = float(sum(cateList[i][j].values()))
            entropySum = 0.0
            if total == 0.0:
                entropySum = -1.0
            else :
                for value in cateList[i][j].values():
                    if value != 0:
                        entropySum = entropySum - (value/total) * math.log10(value/total)
            rtnlist[i][j] = entropySum
    return rtnlist

def getPOIEntropy(curPath, m, n):
    mlist = [[0 for col in range(n)] for row in range(m)] #initialize the matrix to 0
    filePath = os.path.join(curPath, 'NYC_POI', 'RawData', 'new york_anon_locationData_newcrawl.txt')
    with open(filePath) as f:
        lines = f.readlines()
        s = set()
        for line in lines:
            data = line.split(';')[1].strip('()*').split(',')
            lat = float(data[0])
            lon = float(data[1])
            s = s.union([eval(data[2])])
            gridCoor(mlist, lat, lon, m, n, 1)

        cateList = [[dict.fromkeys(s, 0) for col in range(n)] for row in range(m)]
        for line in lines:
            data = line.split(';')[1].strip('()*').split(',')
            lat = float(data[0])
            lon = float(data[1])
            cate = eval(data[2])
            gridCoorCate(cateList, cate, lat, lon, m, n)
       
        entropyMatrix = calEntropy(cateList, m, n)
    return entropyMatrix   

def genFeatureGroup(m,n):
    feature = {
        'WeekDays':{
            '0000-0400':np.zeros((m, n)),
            '0400-0800':np.zeros((m, n)),
            '0800-1200':np.zeros((m, n)),
            '1200-1600':np.zeros((m, n)),
            '1600-2000':np.zeros((m, n)),
            '2000-2400':np.zeros((m, n))
        },
        'WeekEnds':{
            '0000-0400':np.zeros((m, n)),
            '0400-0800':np.zeros((m, n)),
            '0800-1200':np.zeros((m, n)),
            '1200-1600':np.zeros((m, n)),
            '1600-2000':np.zeros((m, n)),
            '2000-2400':np.zeros((m, n))
        }
    }
    return feature
def calFrequencyFeature(row, checkInfeature, checkOutfeature, st, et, m ,n):
   

    if st.weekday() in [0,1,2,3,4]:
        if 0 <= st.hour and st.hour < 4:
            gridCoor(checkOutfeature['WeekDays']['0000-0400'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
        elif 4 <= st.hour and st.hour < 8:
            gridCoor(checkOutfeature['WeekDays']['0400-0800'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
        elif 8 <= st.hour and st.hour < 12:
            gridCoor(checkOutfeature['WeekDays']['0800-1200'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
        elif 12 <= st.hour and st.hour < 16:
            gridCoor(checkOutfeature['WeekDays']['1200-1600'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
        elif 16 <= st.hour and st.hour < 20:
            gridCoor(checkOutfeature['WeekDays']['1600-2000'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
        else:
            gridCoor(checkOutfeature['WeekDays']['2000-2400'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
    else:
        if 0 <= st.hour and st.hour < 4:
            gridCoor(checkOutfeature['WeekEnds']['0000-0400'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)
        elif 4 <= st.hour and st.hour < 8:
            gridCoor(checkOutfeature['WeekEnds']['0400-0800'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)
        elif 8 <= st.hour and st.hour < 12:
            gridCoor(checkOutfeature['WeekEnds']['0800-1200'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)
        elif 12 <= st.hour and st.hour < 16:
            gridCoor(checkOutfeature['WeekEnds']['1200-1600'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)
        elif 16 <= st.hour and st.hour < 20:
            gridCoor(checkOutfeature['WeekEnds']['1600-2000'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)
        else:
            gridCoor(checkOutfeature['WeekEnds']['2000-2400'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)
        
    if et.weekday() in [0,1,2,3,4]:
        if 0 <= et.hour and et.hour < 4:
            gridCoor(checkInfeature['WeekDays']['0000-0400'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
        elif 4 <= et.hour and et.hour < 8:
            gridCoor(checkInfeature['WeekDays']['0400-0800'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
        elif 8 <= et.hour and et.hour < 12:
            gridCoor(checkInfeature['WeekDays']['0800-1200'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
        elif 12 <= et.hour and et.hour < 16:
            gridCoor(checkInfeature['WeekDays']['1200-1600'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
        elif 16 <= et.hour and et.hour < 20:
            gridCoor(checkInfeature['WeekDays']['1600-2000'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
        else:
            gridCoor(checkInfeature['WeekDays']['2000-2400'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.2)
    else:
        if 0 <= et.hour and et.hour < 4:
            gridCoor(checkInfeature['WeekEnds']['0000-0400'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)
        elif 4 <= et.hour and et.hour < 8:
            gridCoor(checkInfeature['WeekEnds']['0400-0800'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)
        elif 8 <= et.hour and et.hour < 12:
            gridCoor(checkInfeature['WeekEnds']['0800-1200'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)
        elif 12 <= et.hour and et.hour < 16:
            gridCoor(checkInfeature['WeekEnds']['1200-1600'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)
        elif 16 <= et.hour and et.hour < 20:
            gridCoor(checkInfeature['WeekEnds']['1600-2000'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)
        else:
            gridCoor(checkInfeature['WeekEnds']['2000-2400'], float(row['start station latitude']), float(row['start station longitude']), m, n, 0.5)

def getBikeFrequency(curPath,m,n):
    checkInfeature = genFeatureGroup(m,n)
    checkOutfeature = genFeatureGroup(m,n)
    folderPath = os.path.join(curPath, 'NYC_Bike', 'RawData')
    for file in os.listdir(folderPath):
        if '.csv' not in file:
            continue
        filePath = os.path.join(folderPath,file)
        with open(filePath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    st = datetime.datetime.strptime(row['starttime'],'%Y-%m-%d %H:%M:%S')
                    et = datetime.datetime.strptime(row['stoptime'],'%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    # print (e)
                    try:
                        st = datetime.datetime.strptime(row['starttime'],'%m/%d/%Y %H:%M:%S')
                        et = datetime.datetime.strptime(row['stoptime'],'%m/%d/%Y %H:%M:%S')
                    except Exception as e:
                        st = datetime.datetime.strptime(row['starttime'],'%m/%d/%Y %H:%M')
                        et = datetime.datetime.strptime(row['stoptime'],'%m/%d/%Y %H:%M')

                calFrequencyFeature(row,checkInfeature, checkOutfeature,st, et, m ,n)
   
    return checkInfeature, checkOutfeature

def main():
    m,n = numOfGrid()
    curPath = os.getcwd()    

    POIDense = getPOIDensity(curPath,m,n)
    POIEntropy = getPOIEntropy(curPath, m, n)

    BikeDense = getBikeDensity(curPath,m,n)
    BikeCheckInFreq, BikeCheckOutFreq = getBikeFrequency(curPath,m,n)

if __name__=="__main__":
    main()