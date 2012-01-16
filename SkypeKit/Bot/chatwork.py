#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

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
			#for key, value in res.info().items():
			#	print key, value
			print url
			exit()

