#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak at no32.tk>
#

import Skype4Py
import os
import time
from SimpleXMLRPCServer import SimpleXMLRPCServer
import sys, socket

os.environ['DISPLAY'] = ":64"
os.environ['XAUTHORITY'] = "/var/www/.Xauthority"

class SkypeIrcBridge():
	def __init__(self):
		self.skype = Skype4Py.Skype()
		self.start()

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
	sv = SimpleXMLRPCServer((socket.gethostname(), int(sys.argv[1])))
	sv.register_instance(SkypeIrcBridge())
	sv.serve_forever()

