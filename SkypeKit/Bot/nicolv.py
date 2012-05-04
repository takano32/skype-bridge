#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#
communities = [
		'co80029', # dark
		'co571107', #test
		]

import urllib2
from BeautifulSoup import BeautifulSoup
import re

# Skype START
from configobj import ConfigObj
CONFIG = ConfigObj('skype-bridge.conf')
ROOM = "#yuiseki/$4425ae72bc11c305"

import xmlrpclib
xmlrpc_host = CONFIG['bot']['xmlrpc_host']
xmlrpc_port = CONFIG['bot']['xmlrpc_port']
DAEMON = xmlrpclib.ServerProxy('http://%s:%s' % (xmlrpc_host, xmlrpc_port))
# Skype END

opener = urllib2.build_opener()

base_url = 'http://com.nicovideo.jp/community/'
texts = []

for community in communities:
	url = base_url + community
	html = opener.open(url).read()
	soup = BeautifulSoup(html)
	title = soup.find('title').text
	com = soup.find('a', {'class': 'community'})
	if com == None: continue
	texts = []
	texts.append('--')
	texts.append(title)
	texts.append(url)
	texts.append(com.text)
	texts.append(com['href'].replace(r'?ref=community', ''))
	text = "\n".join(texts)
	#DAEMON.send_message(ROOM, text)
	print text

