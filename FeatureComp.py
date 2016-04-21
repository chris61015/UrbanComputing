#-*- coding: utf-8 -*-
'''Doc String'''
import math
import os
import datetime
import csv
import geojson
# import math
import numpy as np
import json

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
    # mlist = [[0 for col in range(n)] for row in range(m)] #initialize the matrix to 0
    filePath = os.path.join(curPath, 'NYC_POI', 'RawData', 'new york_anon_locationData_newcrawl.txt')
    with open(filePath) as f:
        lines = f.readlines()
        s = set()
        for line in lines:
            data = line.split(';')[1].strip('()*').split(',')
            lat = float(data[0])
            lon = float(data[1])
            s = s.union([eval(data[2])])
            # gridCoor(mlist, lat, lon, m, n, 1)

        cateList = [[dict.fromkeys(s, 0) for col in range(n)] for row in range(m)]
        for line in lines:
            data = line.split(';')[1].strip('()*').split(',')
            lat = float(data[0])
            lon = float(data[1])
            cate = eval(data[2])
            gridCoorCate(cateList, cate, lat, lon, m, n)
       
        entropyMatrix = calEntropy(cateList, m, n)
    return entropyMatrix   

def genWeeklyFeature(m,n):
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

def genDailyFeature(m,n):
    feature = {
        '0000-0400':np.zeros((m, n)),
        '0400-0800':np.zeros((m, n)),
        '0800-1200':np.zeros((m, n)),
        '1200-1600':np.zeros((m, n)),
        '1600-2000':np.zeros((m, n)),
        '2000-2400':np.zeros((m, n))     
    }
    return feature

def genDFeatWOLocation():
    feature = {
        '0000-0400':{'count':0, 'value':0.0},
        '0400-0800':{'count':0, 'value':0.0},
        '0800-1200':{'count':0, 'value':0.0},
        '1200-1600':{'count':0, 'value':0.0},
        '1600-2000':{'count':0, 'value':0.0},
        '2000-2400':{'count':0, 'value':0.0}     
    }
    return feature

def genHourlyFeature(idList):
    feature = {
        '0000-0100': {ID[0]:0.0 for ID in idList},
        '0100-0200': {ID[0]:0.0 for ID in idList},
        '0200-0300': {ID[0]:0.0 for ID in idList},
        '0300-0400': {ID[0]:0.0 for ID in idList},
        '0400-0500': {ID[0]:0.0 for ID in idList},
        '0500-0600': {ID[0]:0.0 for ID in idList},
        '0600-0700': {ID[0]:0.0 for ID in idList},
        '0700-0800': {ID[0]:0.0 for ID in idList},
        '0800-0900': {ID[0]:0.0 for ID in idList},
        '0900-1000': {ID[0]:0.0 for ID in idList},
        '1000-1100': {ID[0]:0.0 for ID in idList},
        '1100-1200': {ID[0]:0.0 for ID in idList},       
        '1200-1300': {ID[0]:0.0 for ID in idList},
        '1300-1400': {ID[0]:0.0 for ID in idList},
        '1400-1500': {ID[0]:0.0 for ID in idList},
        '1500-1600': {ID[0]:0.0 for ID in idList},
        '1600-1700': {ID[0]:0.0 for ID in idList},
        '1700-1800': {ID[0]:0.0 for ID in idList},
        '1800-1900': {ID[0]:0.0 for ID in idList},
        '1900-2000': {ID[0]:0.0 for ID in idList},
        '2000-2100': {ID[0]:0.0 for ID in idList},
        '2100-2200': {ID[0]:0.0 for ID in idList},
        '2200-2300': {ID[0]:0.0 for ID in idList},
        '2300-2400': {ID[0]:0.0 for ID in idList}
    }
    return feature

def calTimePeriodFeature(row, time, lat, lon,  m ,n , *features):
    for feature in features:
        if time.weekday() in [0,1,2,3,4]:
            if 0 <= time.hour and time.hour < 4:
                gridCoor(feature['WeekDays']['0000-0400'], lat, lon, m, n, 0.2)
            elif 4 <= time.hour and time.hour < 8:
                gridCoor(feature['WeekDays']['0400-0800'], lat, lon, m, n, 0.2)
            elif 8 <= time.hour and time.hour < 12:
                gridCoor(feature['WeekDays']['0800-1200'], lat, lon, m, n, 0.2)
            elif 12 <= time.hour and time.hour < 16:
                gridCoor(feature['WeekDays']['1200-1600'], lat, lon, m, n, 0.2)
            elif 16 <= time.hour and time.hour < 20:
                gridCoor(feature['WeekDays']['1600-2000'], lat, lon, m, n, 0.2)
            else:
                gridCoor(feature['WeekDays']['2000-2400'], lat, lon, m, n, 0.2)
        else:
            if 0 <= time.hour and time.hour < 4:
                gridCoor(feature['WeekEnds']['0000-0400'], lat, lon, m, n, 0.5)
            elif 4 <= time.hour and time.hour < 8:
                gridCoor(feature['WeekEnds']['0400-0800'], lat, lon, m, n, 0.5)
            elif 8 <= time.hour and time.hour < 12:
                gridCoor(feature['WeekEnds']['0800-1200'],lat, lon, m, n, 0.5)
            elif 12 <= time.hour and time.hour < 16:
                gridCoor(feature['WeekEnds']['1200-1600'], lat, lon, m, n, 0.5)
            elif 16 <= time.hour and time.hour < 20:
                gridCoor(feature['WeekEnds']['1600-2000'], lat, lon, m, n, 0.5)
            else:
                gridCoor(feature['WeekEnds']['2000-2400'], lat, lon, m, n, 0.5)

def calDailyFeature(row, time, lat, lon,  m ,n , increment ,*features):
    for feature in features:
        if 0 <= time.hour and time.hour < 4:
            gridCoor(feature['0000-0400'], lat, lon, m, n, increment)
        elif 4 <= time.hour and time.hour < 8:
            gridCoor(feature['0400-0800'], lat, lon, m, n, increment)
        elif 8 <= time.hour and time.hour < 12:
            gridCoor(feature['0800-1200'], lat, lon, m, n, increment)
        elif 12 <= time.hour and time.hour < 16:
            gridCoor(feature['1200-1600'], lat, lon, m, n, increment)
        elif 16 <= time.hour and time.hour < 20:
            gridCoor(feature['1600-2000'], lat, lon, m, n, increment)
        else:
            gridCoor(feature['2000-2400'], lat, lon, m, n, increment)

def countFeature(time, increment, features):
    for feature in features:
        if 0 <= time.hour and time.hour < 4:
            feature['0000-0400']['value'] += increment
            feature['0000-0400']['count'] += 1
        elif 4 <= time.hour and time.hour < 8:
            feature['0400-0800']['value']  += increment
            feature['0400-0800']['count'] += 1
        elif 8 <= time.hour and time.hour < 12:
            feature['0800-1200']['value']  += increment
            feature['0800-1200']['count'] += 1
        elif 12 <= time.hour and time.hour < 16:
            feature['1200-1600']['value']  += increment
            feature['1200-1600']['count'] += 1
        elif 16 <= time.hour and time.hour < 20:
            feature['1600-2000']['value']  += increment
            feature['1600-2000']['count'] += 1
        else:
            feature['2000-2400']['value']  += increment
            feature['2000-2400']['count'] += 1 

def calDFeatWOLocation(time, m,n ,increment,lat = None,lon = None,*features):
    if (lat != None and lon != None):
        col = int(distance(latMax,lon,latMax,lonMin) / gridLength)
        row = int(distance(lat,lonMin,latMax,lonMin) / gridWidth)
        if (row>= 0 and row<m and col>=0 and col<n):
            countFeature(time, increment, features)
        else :
            print('out of boundary')   
    else:
        countFeature(time, increment, features)

def calAvgValue(data):
    for dateKeys, dataValues in data.items():
        for timeKeys, timeValues in dataValues.items(): 
            if timeValues['count'] != 0:
                timeValues['value'] /= timeValues['count']                    

def getBikeFrequency(curPath,m,n):
    checkInfeature = genWeeklyFeature(m,n)
    checkOutfeature = genWeeklyFeature(m,n)
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
                lat = float(row['start station latitude'])
                lon = float(row['start station longitude'])
                calTimePeriodFeature(row, st, lat, lon, m ,n, checkOutfeature)
                calTimePeriodFeature(row, et, lat, lon, m ,n, checkInfeature)
   
    return checkInfeature, checkOutfeature


def getNoiseDense(curPath, m, n):
    dateDict = dict()
    
    filePath = os.path.join(curPath, 'NYC_Noise', 'NYC_NoiseData.csv')
    with open(filePath) as file:
        reader = csv.DictReader(file)
        for row in reader:
            time = datetime.datetime.strptime(row['Created Date'],'%m/%d/%Y %I:%M:%S %p')
            date = time.strftime('%Y-%m-%d')
            if date not in dateDict.keys():
                dateDict[date] = genDailyFeature(m,n)
            if row['Latitude'] != '' and row['Longitude']!='':
                lat = float(row['Latitude'])
                lon = float(row['Longitude'])
                calDailyFeature(row, time, lat, lon, m ,n , 1, dateDict[date])
    return  dateDict           
                
def getPressureFeature(curPath, m, n):
    dateDict = dict()
    dirPath = os.path.join(curPath,'NYC_Weather','AQS')
    for fileName in os.listdir(dirPath):
        if 'hourly_PRESS' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    t = datetime.datetime.strptime(row['Date Local'],'%Y-%m-%d')
                    date = t.strftime('%Y-%m-%d')
                    time = datetime.datetime.strptime(row['Time Local'],'%H:%M')
                    if date not in dateDict.keys():
                        dateDict[date] = genDFeatWOLocation()
                    lat = float(row['Latitude'])
                    lon = float(row['Longitude'])
                    # there are three stations in AQS Pressure Data Set
                    calDFeatWOLocation(time, m,n,float(row['Sample Measurement']),lat,lon,dateDict[date])
        else:
            continue

    # GSOD Data
    dirPath = os.path.join(curPath,'NYC_Weather','GSOD','RawData')
    for fileName in os.listdir(dirPath):
        if 'RawData' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                f = file.readlines()
                del[f[0]]
                for row in f:
                    for i in range(1,5):
                        row = row.replace('  ',' ')
                    cols = row.split(' ')

                    t = datetime.datetime.strptime(cols[2],'%Y%m%d%H%M')
                    date = t.strftime('%Y-%m-%d')
                    if cols[25] != '******':
                        if date not in dateDict.keys():
                            dateDict[date] = genDFeatWOLocation()
                        calDFeatWOLocation(t,m,n,float(cols[25]),None,None,dateDict[date]) 

    #QCLCD Data        
    dirPath = os.path.join(curPath,'NYC_Weather','QCLCD','RawData')
    for fileName in os.listdir(dirPath):
        if '.csv' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                f = file.readlines()
                del[f[0:7]]
                for row in f:
                    cols = row.split(',')

                    if len(cols)!=1:

                        t = datetime.datetime.strptime(cols[1],'%Y%m%d')
                        time = datetime.datetime.strptime(cols[2],'%M%S')
                        date = t.strftime('%Y-%m-%d')

                        if date not in dateDict.keys():
                            dateDict[date] = genDFeatWOLocation()
                        if cols[30] != 'M':
                            #Unit: (INCHES IN HUNDREDTHS)
                            # 1 inch of mercury =33.86 millibars
                            calDFeatWOLocation(time,m,n,float(cols[30]) * 33.86,None,None,dateDict[date]) 

    calAvgValue(dateDict)

    return dateDict

def getRelativeHumidityFeature(curPath, m, n):
    dateDict = dict()
    dirPath = os.path.join(curPath,'NYC_Weather','AQS')
    for fileName in os.listdir(dirPath):
        if 'hourly_RH_DP' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    t = datetime.datetime.strptime(row['Date Local'],'%Y-%m-%d')
                    date = t.strftime('%Y-%m-%d')
                    time = datetime.datetime.strptime(row['Time Local'],'%H:%M')
                    if date not in dateDict.keys():
                        dateDict[date] = genDFeatWOLocation()
                    lat = float(row['Latitude'])
                    lon = float(row['Longitude'])
                    # there are three stations in AQS RH Data Set
                    calDFeatWOLocation(time,m,n,float(row['Sample Measurement']),lat,lon,dateDict[date])

    #QCLCD Data        
    dirPath = os.path.join(curPath,'NYC_Weather','QCLCD','RawData')
    for fileName in os.listdir(dirPath):
        if '.csv' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                f = file.readlines()
                del[f[0:7]]
                for row in f:
                    cols = row.split(',')

                    if len(cols)!=1:

                        t = datetime.datetime.strptime(cols[1],'%Y%m%d')
                        time = datetime.datetime.strptime(cols[2],'%M%S')
                        date = t.strftime('%Y-%m-%d')

                        if date not in dateDict.keys():
                            dateDict[date] = genDFeatWOLocation()
                        if cols[22] != 'M':
                            calDFeatWOLocation(time,m,n,float(cols[22]),None,None,dateDict[date]) 

    calAvgValue(dateDict)
    return dateDict

def getWindFeature(curPath, m, n):
    windSpeedDict = dict()
    windDirectDict = dict()
    dirPath = os.path.join(curPath,'NYC_Weather','AQS')
    for fileName in os.listdir(dirPath):
        if 'hourly_WIND' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    t = datetime.datetime.strptime(row['Date Local'],'%Y-%m-%d')
                    date = t.strftime('%Y-%m-%d')
                    time = datetime.datetime.strptime(row['Time Local'],'%H:%M')
                    if 'Wind Speed' in row['Parameter Name']:
                        if date not in windSpeedDict.keys():
                            windSpeedDict[date] = genDFeatWOLocation()

                        lat = float(row['Latitude'])
                        lon = float(row['Longitude'])
                        calDFeatWOLocation(time,m,n,float(row['Sample Measurement']),lat,lon,windSpeedDict[date])
                    elif 'Wind Direction' in row['Parameter Name']:
                        if date not in windDirectDict.keys():
                            windDirectDict[date] = genDFeatWOLocation()

                        lat = float(row['Latitude'])
                        lon = float(row['Longitude'])
                        calDFeatWOLocation(time,m,n,float(row['Sample Measurement']),lat,lon,windDirectDict[date])  
                    else:
                        print ("Error")       
        else:
            continue
    
    # GSOD Data
    dirPath = os.path.join(curPath,'NYC_Weather','GSOD','RawData')
    for fileName in os.listdir(dirPath):
        if 'RawData' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                f = file.readlines()
                del[f[0]]
                for row in f:
                    for i in range(1,5):
                        row = row.replace('  ',' ')
                    cols = row.split(' ')

                    t = datetime.datetime.strptime(cols[2],'%Y%m%d%H%M')
                    date = t.strftime('%Y-%m-%d')
                    if cols[3] != '***' and cols[3] != '990':
                        if date not in windDirectDict.keys():
                            windDirectDict[date] = genDFeatWOLocation()
                        calDFeatWOLocation(t,m,n,float(cols[3]),None,None,windDirectDict[date]) 

                    if cols[4] != '***':
                        if date not in windSpeedDict.keys():
                            windSpeedDict[date] = genDFeatWOLocation()

                        # 1 knot =1.15077945 miles per hour
                        calDFeatWOLocation(t,m,n,float(cols[4]) / 1.15077945,None,None,windSpeedDict[date]) 

    #QCLCD Data        
    dirPath = os.path.join(curPath,'NYC_Weather','QCLCD','RawData')
    for fileName in os.listdir(dirPath):
        if '.csv' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                f = file.readlines()
                del[f[0:7]]
                for row in f:
                    cols = row.split(',')

                    if len(cols)!=1:

                        t = datetime.datetime.strptime(cols[1],'%Y%m%d')
                        time = datetime.datetime.strptime(cols[2],'%M%S')
                        date = t.strftime('%Y-%m-%d')

                        #WindSpeed
                        if date not in windSpeedDict.keys():
                            windSpeedDict[date] = genDFeatWOLocation()
                        if cols[24] != 'M':
                            # 1 knot =1.15077945 miles per hour
                            calDFeatWOLocation(time,m,n,float(cols[24]) / 1.15077945,None,None,windSpeedDict[date])    

                        #WindDirection
                        if date not in windDirectDict.keys():
                            windDirectDict[date] = genDFeatWOLocation()
                        if cols[26]!= 'M' and cols[26]!='VR ':
                            calDFeatWOLocation(time,m,n,float(cols[26]),None,None,windDirectDict[date])    

    calAvgValue(windSpeedDict)
    calAvgValue(windDirectDict)
    return windSpeedDict, windDirectDict

def getTempFeature(curPath, m, n):
    dateDict = dict()
    dirPath = os.path.join(curPath,'NYC_Weather','AQS')
    for fileName in os.listdir(dirPath):
        if 'hourly_TEMP' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    t = datetime.datetime.strptime(row['Date Local'],'%Y-%m-%d')
                    date = t.strftime('%Y-%m-%d')
                    time = datetime.datetime.strptime(row['Time Local'],'%H:%M')
                    if date not in dateDict.keys():
                        dateDict[date] = genDFeatWOLocation()
                    lat = float(row['Latitude'])
                    lon = float(row['Longitude'])
                    calDFeatWOLocation(time,m,n,float(row['Sample Measurement']),lat, lon,dateDict[date])
    
     # GSOD Data
    dirPath = os.path.join(curPath,'NYC_Weather','GSOD','RawData')
    for fileName in os.listdir(dirPath):
        if 'RawData' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                f = file.readlines()
                del[f[0]]
                for row in f:
                    for i in range(1,5):
                        row = row.replace('  ',' ')
                    cols = row.split(' ')

                    t = datetime.datetime.strptime(cols[2],'%Y%m%d%H%M')
                    date = t.strftime('%Y-%m-%d')
                    if cols[21] != '****':
                        if date not in dateDict.keys():
                            dateDict[date] = genDFeatWOLocation()
                        calDFeatWOLocation(t,m,n,float(cols[21]),None,None,dateDict[date]) 
        else:
            continue     

    #QCLCD Data        
    dirPath = os.path.join(curPath,'NYC_Weather','QCLCD','RawData')
    for fileName in os.listdir(dirPath):
        if '.csv' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                f = file.readlines()
                del[f[0:7]]
                for row in f:
                    cols = row.split(',')

                    if len(cols)!=1:

                        t = datetime.datetime.strptime(cols[1],'%Y%m%d')
                        time = datetime.datetime.strptime(cols[2],'%M%S')
                        date = t.strftime('%Y-%m-%d')

                        if date not in dateDict.keys():
                            dateDict[date] = genDFeatWOLocation()
                        # DryBulbFarenheit
                        calDFeatWOLocation(time,m,n,float(cols[10]),None,None,dateDict[date]) 
       
    calAvgValue(dateDict)

    return dateDict

def getPrecipFeature(curPath, m, n):
    dateDict = dict()
    dirPath = os.path.join(curPath,'NYC_Weather','ASOS','RawData')
    for fileName in os.listdir(dirPath):
        if 'Precipitation' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    t = datetime.datetime.strptime(row['valid'],'%Y-%m-%d %H:%M')
                    date = t.strftime('%Y-%m-%d')
                    if date not in dateDict.keys():
                        dateDict[date] = genDFeatWOLocation()
                    calDFeatWOLocation(t,m,n,float(row['precip_in']), None, None, dateDict[date])
        else:
            continue

    # GSOD Data
    dirPath = os.path.join(curPath,'NYC_Weather','GSOD','RawData')
    for fileName in os.listdir(dirPath):
        if 'RawData' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                f = file.readlines()
                del[f[0]]
                for row in f:
                    for i in range(1,5):
                        row = row.replace('  ',' ')
                    cols = row.split(' ')

                    t = datetime.datetime.strptime(cols[2],'%Y%m%d%H%M')
                    date = t.strftime('%Y-%m-%d')
                    if cols[-5] != '*****' and cols[-5] != '***':
                        if date not in dateDict.keys():
                            dateDict[date] = genDFeatWOLocation()
                        if (cols[-5] == '0.00T*****' or cols[-5] == '0.00T'):
                            cols[-5] = 0.00
                        calDFeatWOLocation(t,m,n,float(cols[-5]),None,None,dateDict[date]) 

    #QCLCD Data        
    dirPath = os.path.join(curPath,'NYC_Weather','QCLCD','RawData')
    for fileName in os.listdir(dirPath):
        if '.csv' in fileName:
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as file:
                f = file.readlines()
                del[f[0:7]]
                for row in f:
                    cols = row.split(',')

                    if len(cols)!=1:

                        t = datetime.datetime.strptime(cols[1],'%Y%m%d')
                        time = datetime.datetime.strptime(cols[2],'%M%S')
                        date = t.strftime('%Y-%m-%d')

                        if date not in dateDict.keys():
                            dateDict[date] = genDFeatWOLocation()
                        if cols[-4] != 'M' and cols[-4] != ' ':
                            if 'T' in cols[-4]:
                                cols[-4] = 0.0
                            calDFeatWOLocation(time,m,n,float(cols[-4]),None,None,dateDict[date]) 
    calAvgValue(dateDict)
    return dateDict

def countBikeRental(time,m,n,sid,increment,lat,lon,feature):
    col = int(distance(latMax,lon,latMax,lonMin) / gridLength)
    row = int(distance(lat,lonMin,latMax,lonMin) / gridWidth)
    if (row>= 0 and row<m and col>=0 and col<n):
        if 0 <= time.hour and time.hour < 1:
            feature['0000-0100'][sid] += increment
        elif 1 <= time.hour and time.hour < 2:
            feature['0100-0200'][sid] += increment
        elif 2 <= time.hour and time.hour < 3:
            feature['0200-0300'][sid] += increment
        elif 3 <= time.hour and time.hour < 4:
            feature['0300-0400'][sid] += increment
        elif 4 <= time.hour and time.hour < 5:
            feature['0400-0500'][sid] += increment
        elif 5 <= time.hour and time.hour < 6:
            feature['0500-0600'][sid] += increment
        elif 6 <= time.hour and time.hour < 7:
            feature['0600-0700'][sid] += increment
        elif 7 <= time.hour and time.hour < 8:
            feature['0700-0800'][sid] += increment
        elif 8 <= time.hour and time.hour < 9:
            feature['0800-0900'][sid] += increment    
        elif 9 <= time.hour and time.hour < 10:
            feature['0900-1000'][sid] += increment
        elif 10 <= time.hour and time.hour < 11:
            feature['1000-1100'][sid] += increment
        elif 11 <= time.hour and time.hour < 12:
            feature['1100-1200'][sid] += increment
        elif 12 <= time.hour and time.hour < 13:
            feature['1200-1300'][sid] += increment        
        elif 13 <= time.hour and time.hour < 14:
            feature['1300-1400'][sid] += increment
        elif 14 <= time.hour and time.hour < 15:
            feature['1400-1500'][sid] += increment
        elif 15 <= time.hour and time.hour < 16:
            feature['1500-1600'][sid] += increment
        elif 16 <= time.hour and time.hour < 17:
            feature['1600-1700'][sid] += increment
        elif 17 <= time.hour and time.hour < 18:
            feature['1700-1800'][sid] += increment
        elif 18 <= time.hour and time.hour < 19:
            feature['1800-1900'][sid] += increment
        elif 19 <= time.hour and time.hour < 20:
            feature['1900-2000'][sid] += increment
        elif 20 <= time.hour and time.hour < 21:
            feature['2000-2100'][sid] += increment    
        elif 21 <= time.hour and time.hour < 22:
            feature['2100-2200'][sid] += increment
        elif 22 <= time.hour and time.hour < 23:
            feature['2200-2300'][sid] += increment
        elif 23 <= time.hour and time.hour < 24:
            feature['2300-2400'][sid] += increment
        else:
            print("wrong")
    else:
        print('out of boundary')   

def genVicinityList(idList, radius):
    ID = [t[0] for t in idList]
    dic = {}
    for i in ID:
        dic[i] = []

    for i in range(len(idList)):
        for j in range(i + 1, len(idList)):
            dist = (distance(idList[i][1], idList[i][2], idList[j][1], idList[j][2]))/1000
            if (dist < 1):
                dic[idList[i][0]].append(idList[j][0])
                dic[idList[j][0]].append(idList[i][0])
    return dic

def calBikeRentFeature(vList, dateDict):
    for dayDict in dateDict.values():
        for timeDict in dayDict.values():
            vals = timeDict.copy()
            for k in vals:
                neighborPoints = vList[k]
                s = 0
                for pt in neighborPoints:
                    s += timeDict[pt]
                vals[k] = s
            timeDict = vals


def getBikeRentFeature(curPath, m, n):
    dateDict = {}
    jsonFilePath = os.path.join(curPath,'NYC_Bike','bike.json')
    with open(jsonFilePath) as data_file:    
        data = json.load(data_file)
        idList = [(dic['id'],dic['latitude'], dic['longitude'])for dic in data['stationBeanList']]
        vList = genVicinityList(idList, 1000)
    
    dirPath = os.path.join(curPath,'NYC_Bike','RawData')
    for fileName in os.listdir(dirPath):
        if '.csv' in fileName and '201407' in fileName:    
            filePath = os.path.join(dirPath, fileName)
            with open(filePath) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        t = datetime.datetime.strptime(row['starttime'],'%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        # print (e)
                        try:
                            t = datetime.datetime.strptime(row['starttime'],'%m/%d/%Y %H:%M:%S')
                        except Exception as e:
                            t = datetime.datetime.strptime(row['starttime'],'%m/%d/%Y %H:%M')

                    date = t.strftime('%Y-%m-%d')
                    if date not in dateDict.keys():
                        dateDict[date] = genHourlyFeature(idList)
                    lat = float(row['start station latitude'])
                    lon = float(row['start station longitude'])
                    if int(row['start station id']) in [ID[0] for ID in idList]:
                        countBikeRental(t,m,n,int(row['start station id']),1,lat,lon,dateDict[date])
                    # else:
                        # print("Non-Valid \"id\":%s" % row['start station id'])
        
        return calBikeRentFeature(vList, dateDict)

def calKappa(cate, ncate, NgammaP, numOfBikeStation):
    NgammaL = numOfBikeStation
    N = NgammaP + NgammaL

    kappa = 0
    for k,v in ncate.items():
        if sum([it[1] for it in v.items()]) != 0.0:
            kappa += v['bike'] / (sum([it[1] for it in v.items()]) - v[cate])

    return  kappa*((N-NgammaP) / (NgammaP*NgammaL))

def calQuality(neighbor, numOfPOI, bikeData):

    avgNgammap = 0
    score = 0
    for cate in neighbor.keys():
        NgammaP = len(neighbor[cate])
        kappa = calKappa(cate, neighbor[cate], NgammaP, len(bikeData['stationBeanList']))
        
        avgNgammap = sum([neighbor['bike'][bikeId][cate] for bikeId in neighbor['bike']]) / len(neighbor['bike'])

        if kappa != 0.0:
            score += math.log10(kappa) * (NgammaP - avgNgammap)
    return score

def countDist(cate, id, cateDict, radius):
    cntDict = {}
    for k in cateDict.keys():
        cntDict.update({k:0.0})

    lon = cateDict[cate][id]['lon']
    lat = cateDict[cate][id]['lat']
     
    for category in cateDict:
        for itemID in cateDict[category]:
            if (category!= cate and itemID != id):
                lon2 = cateDict[category][itemID]['lon']
                lat2 = cateDict[category][itemID]['lat']
                # lat1,lng1,lat2,lng2
                dist = distance(lon, lat, lon2,lat2)/1000
                if (dist <= radius):
                    cntDict[category]+=1
    return cntDict

def countCategory (cate, cateDict):
    idDict = {}
    for itemID in cateDict[cate]:
        idDict[itemID] = countDist(cate, itemID, cateDict, 1)
    return idDict

def countNeighbor(cateDict):
    neighborDict = {}
    for cate in cateDict:
        neighborDict[cate] = countCategory(cate,cateDict)
    return neighborDict

def getPOIBikeQuality(curPath,m,n):
    filePath = os.path.join(curPath, 'NYC_POI', 'RawData', 'new york_anon_locationData_newcrawl.txt')
    with open(filePath) as f:
        lines = f.readlines()
        cateDict = {}
        cnt = 0
        for line in lines:
            if cnt <100:
                id = line.split(';')[0].strip('*')
                data = line.split(';')[1].strip('()*').split(',')
                lat = float(data[0])
                lon = float(data[1])
                category = eval(data[2])
                if eval(data[2]) not in cateDict.keys():
                    cateDict[category] = {id:{'lon':float(data[1]), 'lat':float(data[0]), 'category':category}}
                else:
                    cateDict[category].update({id:{'lon':float(data[1]), 'lat':float(data[0]),'category':category}})
                #
                cnt+=1

        numOfPOI = len(lines)
        # print (cateDict)

    jsonFilePath = os.path.join(curPath,'NYC_Bike','bike.json')
    with open(jsonFilePath) as data_file:    
        bikeData = json.load(data_file)
        bikeDict = {}
        for data in bikeData['stationBeanList']:
            bikeDict.update({data['id']:{'lon':float(data['longitude']), 'lat':float(data['latitude']),'category':'bike'}})
        cateDict['bike'] = bikeDict
 
    Neighbor = countNeighbor(cateDict)  
    # print(Neighbor)      
    quality = calQuality(Neighbor, numOfPOI ,bikeData)

    return quality   



def main():
    m,n = numOfGrid()
    curPath = os.getcwd()    

    # POIDense = getPOIDensity(curPath,m,n)
    # POIEntropy = getPOIEntropy(curPath, m, n)
    POIBikeQuality = getPOIBikeQuality(curPath, m, n)
    # BikeDense = getBikeDensity(curPath,m,n)
    # BikeCheckInFreq, BikeCheckOutFreq = getBikeFrequency(curPath,m,n)

    # NoiseDense = getNoiseDense(curPath, m, n)

    # PressureFeature = getPressureFeature(curPath, m, n)
    # RHFeature = getRelativeHumidityFeature(curPath, m, n)

    # WindSpeedFeature, WindDirectFeature = getWindFeature(curPath, m, n)
    # TempFreature = getTempFeature(curPath, m, n)
    # PrecipFeature = getPrecipFeature(curPath, m, n)
    # PM2_5Freature = getPM2_5Feature(curPath, m, n)

    # BikeRentFeature = getBikeRentFeature(curPath, m, n)


if __name__=="__main__":
    main()