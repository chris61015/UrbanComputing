#-*- coding: utf-8 -*-
import json
import geojson

def findEdgeNode(nodeList):
	ns = sorted(nodeList, key=lambda nodeList: nodeList[1])
	print ("South: lon=%s, lat=%s" % (ns[0][0], ns[0][1]))
	print ("North: lon=%s, lat=%s" % (ns[-1][0], ns[-1][1]))
	
	ew = sorted(nodeList, key=lambda nodeList: nodeList[0])
	print ("West: lon=%s, lat=%s" % (ew[0][0], ew[0][1]))
	print ("Eest: lon=%s, lat=%s" % (ew[-1][0], ew[-1][1]))


def decodeJson(jsonFile):
	with open(jsonFile,'r') as f:
		data = geojson.load(f)
		content = []
		for ds in data['geometry']['coordinates']:
			for subds in ds:
				for sub2ds in subds:
					content.append(sub2ds)
		findEdgeNode(content)
	
 
def main():
	decodeJson("nyc_boundary.geojson")

if __name__=="__main__":
	main()