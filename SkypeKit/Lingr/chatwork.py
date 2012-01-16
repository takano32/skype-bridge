#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

import json

from configobj import ConfigObj
CONFIG = ConfigObj('skype-bridge.conf')
ROOM = "arakawatomonori"
VERIFIER = CONFIG['lingr']['verifier']

def say(room, text, verifier):
	request = "http://lingr.com/api/room/say?room=%s&bot=%s&text=%s&bot_verifier=%s"
	request  = request % (room, 'skype', text, verifier)
	try:
		response = urllib2.urlopen(request)
	except urllib2.HTTPError as err:
		print 'urllib2.HTTPError: %s' % time.ctime(time.time())
		time.sleep(3)
		say(room, text, verifier)
		return
	if response.code == 200:
		res = json.JSONDecoder().decode(response.read())
		if res.has_key('status'):
			if res['status'] == 'ok':
				return
			else:
				pass

import urllib2
import random
class HeadRequest(urllib2.Request):
	def get_method(self):
		return "HEAD"

while True:
	x = int(random.random() * 3)
	y = int(random.random() * 3800)
	for ext in ['jpg', 'png', 'gif']:
		url = 'http://chat-work-appdata.s3.amazonaws.com/icon/%d/%d.%s' % (x, y, ext)
		request = HeadRequest(url)
		try:
			res = urllib2.urlopen(request)
		except Exception as err:
			continue

		if res.code == 200:
			say(ROOM, url, VERIFIER)
			exit()

