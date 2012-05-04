#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#
communities = [
		'co80029', # dark
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
	html = opener.open(base_url + community).read()
	soup = BeautifulSoup(html)
	com = soup.find('a', {'class': 'community'}).text
	print com
	#texts.append("%-12s %-16s %12s %s w/ %-s %s" % (code, com, l, unit, c, cp) )

#text = "\n".join(texts)
#DAEMON.send_message(ROOM, text)

