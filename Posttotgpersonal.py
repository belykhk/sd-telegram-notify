# -*- coding: utf-8 -*-
#########################
# Author - Kostya Belykh#
#	   k@belykh.su      #
#########################
import settings
import requests
import os
import sys
import ssl
import random
import json
import datetime
import socks
import socket

# Proxy settings, Socks5
if settings.proxy_use == True:
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, settings.proxy_server, int(settings.proxy_port), True, settings.proxy_username, settings.proxy_password)
	socket.socket = socks.socksocket

import urllib
import urllib2

reload(sys)
sys.setdefaultencoding('utf8')

# Reading the argument passed to the script.The Request details are stored as a JSON Object in a file and its path is provided to the Script as input.
file = str(sys.argv[1])
# filename = c:\\ManageEngine\\ServiceDesk\\integration\\custom_scripts\\new.json

# Reading the Request JSON object from the json file which is provided as input to the script as $COMPLETE_JSON_FILE.
with open(file) as data_file:
	data = json.load(data_file)
requestObj = data['request']

# Assigning value got from the Request fields to variables.
workorderid = requestObj['WORKORDERID']
createdby = requestObj['REQUESTER']
priority = requestObj['PRIORITY']
technician = requestObj['TECHNICIAN']
dep = requestObj['DEPARTMENT']
subject = requestObj['SUBJECT']
description = requestObj['SHORTDESCRIPTION']

# Selecting user to send notofocation
for row in settings.tech_arr:
	if technician == row[0]:
		uid = str(row[1])

# Convert time from timestamp to readable format, eg 01 jan 2018, 21:45:00
CREATEDTIME = requestObj['CREATEDTIME']
requestcreationtime=datetime.datetime.fromtimestamp(int(CREATEDTIME) / 1e3).strftime('%d %b %Y, %H:%M:%S')
DUEBYTIME = requestObj['DUEBYTIME']
requestduetime=datetime.datetime.fromtimestamp(int(DUEBYTIME) / 1e3).strftime('%d %b %Y, %H:%M:%S')

# This is the actual message content and can be updated based on your requirement.
message = "Got new reply on request " + workorderid +\
	"\n<b>Subject: </b>" + subject +\
	"\n<b>Deadline: </b>" + requestduetime + \
	"\n\n<b>Author: </b>" + createdby +\
	"\n<b>Department: </b>" + dep + \
	"\n<b>Link: </b>" + settings.sd_url + '''/WorkOrder.do?woMode=viewWO&woID=''' + workorderid

# Evil Hack to urllib2 ssl check
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Request latest messages
result = urllib2.urlopen("https://api.telegram.org/bot" + settings.tg_bot_key + "/getUpdates", context=ctx).read()

# Send a message to a chat room (chat room ID retrieved from getUpdates)
result = urllib2.urlopen("https://api.telegram.org/bot" + settings.tg_bot_key + "/sendMessage", urllib.urlencode({"chat_id" : uid, "text" : message, "parse_mode" : "HTML"}), context=ctx).read()

