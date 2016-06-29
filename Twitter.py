#-*- coding: utf-8 -*-
import json
import oauth2
import urllib
import collections

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""

def oauth_req(url,http_method="GET",post_body="".encode('utf-8'),http_headers=None):
	consumer=oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	token=oauth2.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client=oauth2.Client(consumer, token)
	resp,content=client.request(url,method=http_method,body=post_body,headers=http_headers)
	return content.decode(encoding='UTF-8')

def main():
	with open('token.json') as data_file:
		tokenData = json.load(data_file)

	global ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET
	ACCESS_KEY = tokenData['AccessToken']
	ACCESS_SECRET = tokenData['AccessTokenSecret']
	CONSUMER_KEY = tokenData['ConsumerKey']
	CONSUMER_SECRET = tokenData['ConsumerSecret']

	search = urllib.parse.urlencode({'q':'','geocode':'40.744873,-73.99651,1km'})
	st = search + "%20since%3A2014-07-01%20until%3A2015-06-30"
	print (st)
	url = ("https://api.twitter.com/1.1/search/tweets.json?%s" % st)
	print (url)

	rtnJson = json.loads(oauth_req(url,"GET"))
	s = json.dumps(rtnJson,sort_keys = True)
	print(s)
if __name__=="__main__":
	main()