#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

codes = [
		'NASDAQ:AKAM', # Akamai
		'NASDAQ:GOOG', # Google
		'NASDAQ:AAPL', # Apple
		'NASDAQ:YHOO', # Yahoo!
		'TYO:4689',    # Yahoo! Japan
		'TYO:3632',    # GREE
		'TYO:2432',    # DeNA
		'TYO:2121',    # mixi
		'TYO:4751',    # CyberAgent
		'TYO:3715',    # Dwango
		'TYO:2193',    # COOKPAD
		'TYO:7733',    # OLYMPUS
		'TYO:6501',    # Hitachi
		]

import urllib2
from BeautifulSoup import BeautifulSoup
import re

# Skype START
from configobj import ConfigObj
CONFIG = ConfigObj('../skype-bridge.conf')
ROOM = "#yuiseki/$4425ae72bc11c305"

import xmlrpclib
xmlrpc_host = CONFIG['bot']['xmlrpc_host']
xmlrpc_port = CONFIG['bot']['xmlrpc_port']
DAEMON = xmlrpclib.ServerProxy('http://%s:%s' % (xmlrpc_host, xmlrpc_port))
# Skype END

opener = urllib2.build_opener()

base_url = 'http://www.google.com/finance?q='
texts = [base_url]
for code in codes:
	html = opener.open(base_url + code).read()
	soup = BeautifulSoup(html)
	com = soup.find('h3').text.replace('&nbsp;', '').split()[:1][0]
	l  = soup.find(id = re.compile('ref_[0-9]+_l')).text
	unit = 'JPY'
	if code.startswith('NASDAQ'): unit = 'USD'
	c  = soup.find(id = re.compile('ref_[0-9]+_c')).text
	cp = soup.find(id = re.compile('ref_[0-9]+_cp')).text
	code = '[%s]' % code
	texts.append("%-12s %-16s %12s %s w/ %-s %s" % (code, com, l, unit, c, cp) )

text = "\n".join(texts)
DAEMON.send_message(ROOM, text)

