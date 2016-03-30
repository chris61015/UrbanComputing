"""This script is for crawling Quality Controlled Local Climatological Data (QCLCD) from website"""
#encoding=utf8
import os
import urllib
import urllib2
import datetime
import time
from bs4 import BeautifulSoup
from dateutil import rrule

def searchPeriod(startTime, endTime):
	"""input format:yyyymm, it returns a list of dates between starttime and endtime"""
	#turn string into datetime
	st = datetime.datetime.strptime(startTime, '%Y%m')
	et = datetime.datetime.strptime(endTime, '%Y%m')

	#run rrule for add one month to st on every loop until it reachs et
	rtnList = []
	for date in rrule.rrule(rrule.MONTHLY, dtstart=st, until=et):
		rtnList.append(date.strftime('%Y%m')[-4:])
	return rtnList	

def writeFile(path, dic, content):
	"""Write CSV files to a specified directory"""
	fileName = '%s_%s_%s.csv' % (dic['state'], dic['callsign'],dic['VARVALUE'][-4:])
	with open(os.path.join(path,'QCLCD',fileName),'w' )as f:
		f.writelines(content)

def parseWebsite(url, state, sites, searchStr, path, paramList):
	"""Crawl content from website"""
	for site in sites:
		#enter Year-Month selection page for a specific observation site
		paramList.update(state)
		paramList.update(site)
		post_args = urllib.urlencode(paramList)
		fp = urllib2.urlopen(url, post_args)
		soup = BeautifulSoup(fp, 'html.parser')

		#Make a list of html option tags of specified Year-Month 
		YearMonthList = []
		for option in soup.find_all('option'):
			value = option.get('value')
			if value[-4:] in searchStr:
				YearMonthList.append({'VARVALUE':value})

		#enter date selection page for a specific Year-Month and site
		for ym in YearMonthList:
			year_param = paramList.copy()
			year_param.update(ym)
			year_args = urllib.urlencode(year_param)
			ws = urllib2.urlopen(url, year_args)
			selDayPage = BeautifulSoup(ws, 'html.parser')

			# try to be a nice guy
			time.sleep(1)

			#send request to get data
			day_param = year_param.copy()
			day_param.update({'reqday':'E'})
			day_param.update({'which':'ASCII Download (Hourly Obs.) (10A)'})
			day_args = urllib.urlencode(day_param)
			ds = urllib2.urlopen(url, day_args)
			dataPage = BeautifulSoup(ds, 'html.parser')

			#write csv file in folder
			writeFile(path,day_param, dataPage.pre.string)
			
		#clear the parameterlist or it will be updated and become longer in each loop 
		paramList.clear()

if __name__ == '__main__':
	state = {'state':'NY'}
	#obeservation sites
	sites = [{'callsign':'LGA'},{'callsign':'NYC'},{'callsign':'JFK'}]
	searchStr = searchPeriod('201406','201506')

	path = os.getcwd()

	paramList = {}
	url = 'http://www.ncdc.noaa.gov/qclcd/QCLCD?prior=N'

	parseWebsite(url, state, sites, searchStr, path, paramList)
