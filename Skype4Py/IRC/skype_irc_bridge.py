#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak at no32.tk>
#

import Skype4Py
import os
import time

os.environ['DISPLAY'] = ":64"
os.environ['XAUTHORITY'] = "/var/www/.Xauthority"

class SkypeIrcBridge():
	def __init__(self):
		self.skype = Skype4Py.Skype()

	@staticmethod
	def handler(msg, event):
		if event == u"RECEIVED":
			print "ChatName %s" % msg.ChatName
			print "Body %s" % msg.Body
			print ""

	def start(self):
		self.skype.OnMessageStatus = SkypeIrcBridge.handler
		self.skype.Attach()

if __name__ == "__main__":
	bridge = SkypeIrcBridge()
	bridge.start()
	while True:
		time.sleep(0.5)

