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
from configobj import ConfigObj
import sys, xmlrpclib

os.environ['DISPLAY'] = ":16"
os.environ['XAUTHORITY'] = "/home/takano32/.Xauthority"

CONFIG = ConfigObj("bridge.conf")

class SkypeIrcBridge():
	xmlrpc_host = CONFIG['irc']['xmlrpc_host']
	xmlrpc_port = CONFIG['irc']['xmlrpc_port']
	irc = xmlrpclib.ServerProxy('http://%s:%s' % (xmlrpc_host, xmlrpc_port))
	def __init__(self):
		self.skype = Skype4Py.Skype()
		self.start()

	@staticmethod
	def handler(msg, event):
		if len(msg.Body) == 0:
			return
		if event == u"RECEIVED":
			for key in CONFIG:
				if key == 'skype' or key == 'irc':
					continue
				if CONFIG[key].has_key('skype') and msg.ChatName == CONFIG[key]['skype']:
					name = msg.Sender.FullName
					if len(name) == 0 or len(name) > 16:
						name = msg.Sender.Handle
					if CONFIG[key].has_key('irc'):
						channel = CONFIG[key]['irc']
						for line in msg.Body.splitlines():
							text = '%s: %s' % (name, line)
							print "before"
							SkypeIrcBridge.irc.say(channel, text.encode('utf-8'))
							print "after"
							if WAIT != None:
								time.sleep(WAIT)
							else:
								time.sleep(len(text) / 20.0)

	@staticmethod
	def inspect_handler(msg, event):
		if event == u"RECEIVED":
			print "ChatName %s" % msg.ChatName
			print "Body %s" % msg.Body
			print ""
#
	def say(self, channel, msg):
		room = self.skype.Chat(channel)
		room.SendMessage(msg)
		return True

	def start(self):
		self.skype.OnMessageStatus = SkypeIrcBridge.handler
		self.skype.Attach()

if __name__ == "__main__":
	host = CONFIG['skype']['xmlrpc_host']
	port = CONFIG['skype']['xmlrpc_port']
	sv = SimpleXMLRPCServer((host, int(port)))
	sv.register_instance(SkypeIrcBridge())
	sv.serve_forever()

