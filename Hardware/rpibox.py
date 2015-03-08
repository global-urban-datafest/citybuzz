#!/usr/bin/python

import RPi.GPIO as GPIO
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
import urllib
import urllib2
import json



#################
# BOX constants #
#################
boxId = 1
boxLatitude = 53.3430708
boxLongitude = -6.2747221
questionId = ""
question = ""
loop = False

#Setup LCD
lcd = Adafruit_CharLCD()
lcd.begin(16, 1)

#Setup Input pins
redButton = 4
greenButton = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(redButton, GPIO.IN)
GPIO.setup(greenButton, GPIO.IN)

#Functions
#cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
#def run_cmd(cmd):
#    p = Popen(cmd, shell=True, stdout=PIPE)
#    output = p.communicate()[0]
#    return output

def requestQuestion():
	global questionId, question
	print("Requesting current question...")
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
	print("Question received! current question is: " + question + " with ID: " + questionId)
	mainLoop()

def sendResponse(response):

	responseStr = "true"
	responseLabel = "YES"
	if response == False:
		responseStr = "false"
		responseLabel = "NO"

	print("New response: " + responseLabel)
	req = urllib2.Request("https://api.parse.com/1/classes/Responses",
                  headers = { "X-Parse-Application-Id" : "UzuNpxqIsLJIH8c2IFdKo0ifGEkD95pu5AV5bBmf",
                  "X-Parse-REST-API-Key" : "OSxv3JZH59IyoXE2Fof5RnJGiKhIXMv3lAcdUwoG",
                  "Content-Type" : "application/json"
                  },
                  data = '{"question":{"__type": "Pointer", "className": "Questions", "objectId": "' + questionId + '"}, "response":' + responseStr + ', "deviceType":"box", "deviceId":"' + str(boxId) + '", "location": {"__type": "GeoPoint", "latitude":'+ str(boxLatitude) +',"longitude": '+ str(boxLongitude) +'}}')
	f = urllib2.urlopen(req)
	print("Response sent!")
	lcd.clear()
	lcd.message("Response sent:\n" + responseLabel)
	sleep(1.5)
	mainLoop()

#Main function
def mainLoop():

	global loop
	loop = True

	lcd.clear()
	if len(question) > 16:
		lcd.message(question[:16] + "\n" + question[16:])
	else :
		lcd.message(question)
	try:
		while loop:
			if GPIO.input(redButton):
				#print "RED button is 1/GPIO.HIGH/True"
				loop = False
				sendResponse(False)
			if GPIO.input(greenButton):
				#print "GREEN button is 1/GPIO.HIGH/True"
				loop = False
				sendResponse(True)

			sleep(1)

	except KeyboardInterrupt:
			print "\n Program stopped by user\n"

	#except:
			#print "\n Unknown exception occurred\n"

	finally:
		GPIO.cleanup()

#App main start
requestQuestion()

#END
