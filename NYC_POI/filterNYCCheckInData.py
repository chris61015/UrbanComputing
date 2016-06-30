# -*- coding: utf-8 -*-
import os
import csv
import datetime

def main():
    checkInData = []
    venueData = []
    cateData = []
    curPath = os.getcwd()
    dirPath = os.path.join(curPath, 'RawData','Foursquare&Flickr_in_20_cities')
    checkInFilePath = os.path.join(dirPath,'checkins.csv')
    venueFilePath = os.path.join(dirPath,'venues.csv')
    cateFilePath = os.path.join(dirPath,'categories_names.csv')
    
    st = datetime.datetime.strptime('2013-07-01','%Y-%m-%d')
    et = datetime.datetime.strptime('2014-07-01','%Y-%m-%d')

    with open(checkInFilePath, encoding = 'utf8') as checkInFile:
        lines = checkInFile.readlines()
        checkInData.append(lines[0])
        for i in range(1,len(lines)):
            data = lines[i].strip('\n').split(',')
            time = datetime.datetime.strptime(data[2],'%Y-%m-%dT%H:%M:%S')
            if (time >= st and time <et) and (data[3] == 'newyork'):
                checkInData.append(lines[i])

    with open(venueFilePath, encoding = 'utf8') as venueFile:
        lines = venueFile.readlines()
        venueData.append(lines[0])
        for i in range(1,len(lines)):
            data = lines[i].strip('\n').split(',')
            if data[-2] == 'newyork':
                venueData.append(lines[i])      
    
    vidList = [venueRow.strip('\n').split(',')[-1] for venueRow in venueData]

    with open(cateFilePath, encoding = 'utf8') as cateFile:
        lines = cateFile.readlines()
        for i in range(0,len(lines)):
            data = lines[i].strip('\n').split(',')
            if data[0] in vidList:
                cateData.append(lines[i])       
    
    
    with open("NYCCheckins.csv", 'w') as ofile:
        ofile.write(checkInData[0])
        checkIn = sorted(checkInData[1:], key=lambda row: row.split(',')[2])
        # s = sorted(checkIn, key=lambda row: int(row.split(',')[0]))
        ofile.writelines(checkIn)
    
    with open("NYCVenues.csv", 'w', encoding = 'utf8') as f:
        f.writelines(venueData)
    
    with open("NYCCategories.csv", 'w', encoding = 'utf8') as f:
        f.writelines(cateData)

if __name__ == '__main__':
    main()