#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#
communities = [
		'co80029',   # Dark
		'co1513375', # Light
		'co600306',  # np-complete
		'co9320',    # プログラミング生放送
		'co1495908', # JK
		# 'co244678',  # 神回
		# 'co23655',   # アリーナ
		# 'co1024634', # まるはに
		# 'co405315',  # プログラマ
		]

ROOMS = [
		'#yuiseki/$4425ae72bc11c305',
		#'#pha_pha_/$7604f24b1d42a542',
		#"#takano32/$d380f06c719822e7",
		]

import urllib2
from BeautifulSoup import BeautifulSoup
import re, time

# Skype START
from configobj import ConfigObj
CONFIG = ConfigObj('skype-bridge.conf')

import xmlrpclib
xmlrpc_host = CONFIG['bot']['xmlrpc_host']
xmlrpc_port = CONFIG['bot']['xmlrpc_port']
DAEMON = xmlrpclib.ServerProxy('http://%s:%s' % (xmlrpc_host, xmlrpc_port))
# Skype END

opener = urllib2.build_opener()

base_url = 'http://com.nicovideo.jp/community/'

latest_urls = {}
for community in communities:
	latest_urls[community] = None

while True:
	for community in communities:
		url = base_url + community
		try:
			html = opener.open(url).read()
		except Exception as err:
			print err
			print community
			print
			continue
		soup = BeautifulSoup(html)
		title = soup.find('title').text
		link = soup.find('a', {'class': 'community'})
		if link == None: continue
		texts = []
		# community
		#texts.append(title)
		#texts.append(url)
		texts.append(link.text)
		href = link['href'].replace(r'?ref=community', '')
		texts.append(href)
		texts.append('--')
		text = "\n".join(texts)
		if latest_urls[community] == href: continue
		latest_urls[community] = href

		for room in ROOMS:
			DAEMON.send_message(room, text)
		#print text
	time.sleep(30.0)
	print time.ctime(time.time())

