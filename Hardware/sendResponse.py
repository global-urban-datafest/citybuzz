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
boxLatitude = 53.338907
boxLongitude = -6.186179
questionId = ""
response = "0"

if len(sys.argv) > 1:
    questionId = sys.argv[1]
    response = sys.argv[2]
    #print questionId


dataTest = '{"appID": "2","question_id": "' + questionId + '","answer": "' + response + '","category": "Polling","coordX": "' + str(boxLatitude) + '","coordY": "' + str(boxLongitude) + '"}'
print dataTest

#Local instance vs Server instance
#http://citybuzz.mybluemix.net
#http://172.16.10.217:3000
req = urllib2.Request("http://172.16.10.217:3000/putAnswer",
              headers = {"Content-Type" : "application/json"
              },
              data = '{"appID": "2","question_id": "' + questionId + '","answer": "' + response + '","category": "Polling","coordX": "' + str(boxLatitude) + '","coordY": "' + str(boxLongitude) + '"}')
f = urllib2.urlopen(req)
print("Response sent!")

#END
