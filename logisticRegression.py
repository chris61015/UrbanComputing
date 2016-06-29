#-*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier
from sklearn.linear_model import LogisticRegression

 
def predictHalfTime(x,y):
	numOfDataset = len(y)/2

	trainX = x.iloc[:numOfDataset,:].values 
	testX  = x.iloc[numOfDataset:,:].values

	trainY = y.iloc[:numOfDataset].values 
	testY = y.iloc[:numOfDataset].values 

	OVR = OneVsRestClassifier(LogisticRegression()).fit(trainX,trainY)
	OVO = OneVsOneClassifier(LogisticRegression()).fit(trainX,trainY)

	print ('One vs rest accuracy: %f' % OVR.score(testX,testY))
	print ('One vs one accuracy: %f' % OVO.score(testX,testY))

	print("===============================")

def predictHalfPlace(x,y):
	numOfDataset = len(y)/2

	trainX = x.iloc[0::2,:].values
	testX  = x.iloc[1::2,:].values

	trainY = y.iloc[0::2].values
	testY = y.iloc[1::2].values

	# print (x,y)
	# print (trainX, trainY)
	# print (testX, testY)

	OVR = OneVsRestClassifier(LogisticRegression()).fit(trainX,trainY)
	OVO = OneVsOneClassifier(LogisticRegression()).fit(trainX,trainY)

	print ('One vs rest accuracy: %f' % OVR.score(testX,testY))
	print ('One vs one accuracy: %f' % OVO.score(testX,testY))

	print("===============================")

def predictRandom(x,y):
	numOfDataset = len(y)/2
	fullInx = x.index

	trainInx = np.random.choice(fullInx, numOfDataset,replace=False)
	mask = np.in1d(fullInx, trainInx, invert=True)

	testInx = fullInx[mask]

	trainX = x.iloc[trainInx,:].values
	testX  = x.iloc[testInx,:].values

	trainY = y.iloc[trainInx].values
	testY = y.iloc[testInx].values

	# print (x,y)
	# print (trainX, trainY)
	# print (testX, testY)

	OVR = OneVsRestClassifier(LogisticRegression()).fit(trainX,trainY)
	OVO = OneVsOneClassifier(LogisticRegression()).fit(trainX,trainY)

	print ('One vs rest accuracy: %f' % OVR.score(testX,testY))
	print ('One vs one accuracy: %f' % OVO.score(testX,testY))

	print("===============================")	

def main():
	# load the CSV file as a numpy matrix
	# dataset = np.loadtxt("NoiseDataSet.txt", delimiter=",")
	name=['Date', 'Time', 'M','N','POIDense','POIEntropy','BikeDense','DailyCheckOut','DailyCheckIn','Pressure','WindSpeed','WindDirect','Temperatue','PM2.5','PM10','CheckInPop','CheckInTransit','CheckInIncomingFlow','NoiseDense']

	data = pd.read_csv('NoiseDataSet.txt', sep=",", header = None, names=name)

	# separate the data from the target attributes
	x = data.iloc[:,4:18]
	y = data.iloc[:,18]

	predictHalfTime(x,y)
	predictHalfPlace(x,y)
	predictRandom(x,y)

if __name__=="__main__":
	main()