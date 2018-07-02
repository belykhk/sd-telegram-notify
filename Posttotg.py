# -*- coding: utf-8 -*-
#########################
# Author - Kostya Belykh#
#      k@belykh.su      #
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
filename = str(sys.argv[1])
# filename = c:\\ManageEngine\\ServiceDesk\\integration\\custom_scripts\\new.json

# Reading the Request JSON object from the json file which is provided as input to the script as $COMPLETE_JSON_FILE.
with open(filename) as data_file:
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

# Add telegram nickname for notification
for row in settings.tech_arr:
	if technician == row[0]:
		technician = row[0] + " " + row[2]

# Convert time from timestamp to readable format, eg 01 jan 2018, 21:45:00
CREATEDTIME = requestObj['CREATEDTIME']
requestcreationtime=datetime.datetime.fromtimestamp(int(CREATEDTIME) / 1e3).strftime('%d %b %Y, %H:%M:%S')
DUEBYTIME = requestObj['DUEBYTIME']
requestduetime=datetime.datetime.fromtimestamp(int(DUEBYTIME) / 1e3).strftime('%d %b %Y, %H:%M:%S')

# This is the actual message content and can be updated based on your requirement.
message = "New ticket with priority " + "<b>" + priority + "</b>" + \
	"\n<b>Ticket No.: </b>" + workorderid + \
	"\n<b>Technician: </b>" + technician + \
	"\n<b>Subject: </b>" + subject +\
	"\n\n<b>Created: </b>" + requestcreationtime + \
	"\n<b>Deadline: </b>" + requestduetime + \
	"\n\n<b>Author: </b>" + createdby +\
	"\n<b>Department: </b>" + dep + \
	"\n<b>Link: </b>" + settings.sd_url + '''/WorkOrder.do?woMode=viewWO&woID=''' + workorderid + \
	"\n\n<b>Description: </b>\n" + description

# Evil Hack to urllib2 ssl check
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Request latest messages
result = urllib2.urlopen("https://api.telegram.org/bot" + settings.tg_bot_key + "/getUpdates", context=ctx).read()

# Send a message to a chat room (chat room ID retrieved from getUpdates)
result = urllib2.urlopen("https://api.telegram.org/bot" + settings.tg_bot_key + "/sendMessage", urllib.urlencode({"chat_id" : settings.group_chat_id, "text" : message, "parse_mode" : "HTML"}), context=ctx).read()

# Sending sticker if priority = high
if priority == settings.high_priority:
    # Choosing it
    randsticker = random.choice(settings.stickers)
    # Sending it
    result = urllib2.urlopen("https://api.telegram.org/bot" + settings.tg_bot_key + "/sendSticker", urllib.urlencode({ "chat_id": settings.group_chat_id, "sticker": randsticker }), context=ctx).read()

