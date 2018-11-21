import json
from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import urllib2
import sys
import threading
import time

channels = json.load(open('domainChannels.json'))

chan = {}
count=0
for channel in channels.keys():
	# count+=1
	# if count>=2:
	# 	break
	print "channel"
	chanVids = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/search?key=AIzaSyClserQ1cuNOX9SssQT6-BvBf65JZZ1Lk4&channelId="+channel+"&part=snippet,id&order=date&maxResults=50").read())
	# d = []
	print str(100*(count/float(len(channels.keys()))))[:4]+'%'

	title = []
	channelId = []
	channelTitle = []
	categoryId = []
	videoId = []
	viewCount = []
	commentCount = []
	category = []
	videos = []
	comments = []
	tags = []
	description = []
	chan['channel']={}
	for k in range(len(chanVids['items'])):
		if 'videoId' in chanVids['items'][k]['id']:
			videoId.append('https://www.youtube.com/watch?v='+chanVids['items'][k]['id']['videoId'])
			title.append(chanVids['items'][k]['snippet']['title']) 
			try:
				categoryId.append(chanVids['items'][k]['snippet']['categoryId'])
			except:
				categoryId.append('No categoryId')
			try:
				viewCount.append(chanVids['items'][k]['statistics']['viewCount'])
			except:
				viewCount.append('No viewCount')
			try:
				tags.append(chanVids['items'][k]['snippet']['tags'])
			except:
				tags.append('No tags')
			try:
				description.append(chanVids['items'][k]['snippet']['description'])
			except:
				description.append('No description')
			try:
				commentsOnVideo = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74&textFormat=plainText&part=snippet&videoId=" + chanVids['items'][k]['id']['videoId'] + "&maxResults=50",timeout=60).read())
				c = []
				for k in range(len(commentsOnVideo['items'])):
					c.append(commentsOnVideo['items'][k]["snippet"]['topLevelComment']['snippet']['textDisplay'])
				comments.append(c)
			except:
			    comments.append('No comments')
			try:
			    if 'commentCount' in chanVids['items'][k]['statistics'].keys():
			        commentCount.append(chanVids['items'][k]['statistics']['commentCount'])
			    else:
			        commentCount.append("No commentCount")
			except:
			    commentCount.append("No commentCount")

	chan['channel']['title']=title
	chan['channel']['categoryId']=categoryId
	chan['channel']['videoId']=videoId
	chan['channel']['viewCount']=videoId
	chan['channel']['commentCount']=commentCount
	chan['channel']['comments']=comments
	chan['channel']['tags']=tags
	chan['channel']['description']=description


	# break
# print chan
with open('domainChannelsVideos.json','w') as f:
	json.dump(chan,f)		        
# if response['items'][0]['snippet']['channelId'] not in chan:
#     chan[response['items'][0]['snippet']['channelId']] = d
