#!/usr/bin/python

from subprocess import *
from time import sleep, strftime
from datetime import datetime
import urllib
import urllib2
import json
import sys

#################
# BOX constants #
#################
boxId = 1
boxLatitude = 53.3430708
boxLongitude = -6.2747221
questionId = ""
question = ""


if len(sys.argv) > 1:
    questionParam = sys.argv[1]
    #print questionId


#Local instance vs Server instance
#http://citybuzz.mybluemix.net
#http://172.16.10.217:3000
req = urllib2.Request('http://172.16.10.217:3000/getLastQuestion?category=Polling',
              headers = {"Content-Type" : "application/json"
              })
response = urllib2.urlopen(req)
responseData = json.load(response)
questionId = responseData["res"][0]["_id"]
question = responseData["res"][0]["question"]

print questionId

if len(question) > 16:
    print question[:16]
    print question[16:32]
else :
    print question
    print "                "

#END
