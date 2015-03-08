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
    questionId = sys.argv[1]
    #print questionId

params = urllib.urlencode({"where":json.dumps({"targetBox": str(boxId)}),"order":"startDate","limit":"1"})

req = urllib2.Request('https://api.parse.com/1/classes/Questions?%s' % params,
              headers = { "X-Parse-Application-Id" : "UzuNpxqIsLJIH8c2IFdKo0ifGEkD95pu5AV5bBmf",
              "X-Parse-REST-API-Key" : "OSxv3JZH59IyoXE2Fof5RnJGiKhIXMv3lAcdUwoG",
              "Content-Type" : "application/json"
              })
response = urllib2.urlopen(req)
responseData = json.load(response)
questionId = responseData["results"][0]["objectId"]
question = responseData["results"][0]["question"]

print questionId

if len(question) > 16:
    print question[:16]
    print question[16:32]
else :
    print question

#END
