#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

import Skype4Py
from configobj import ConfigObj
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import os

os.environ['DISPLAY'] = ":64"
os.environ['XAUTHORITY'] = "/home/www/.Xauthority"

CONFIG = ConfigObj("/home/takano32/workspace/skype-bridge/Skype4Py/skype-bridge.conf")

class SendMessage():
	def __init__(self):
		self.skype = Skype4Py.Skype()
		self.skype.Attach()
		self.lock = threading.Lock()

	def send_message(self, room, msg):
		with self.lock:
			room = self.skype.Chat(room)
			room.SendMessage(msg)
		return True

	def re_attach(self):
		self.skype.ResetCache()
		self.skype = Skype4Py.Skype()
		self.skype.Attach()
		return True

if __name__ == "__main__":
	host = CONFIG['skype']['xmlrpc_host']
	port = CONFIG['skype']['xmlrpc_port']
	sv = SimpleXMLRPCServer((host, int(port)))
	sv.register_instance(SendMessage())
	sv.serve_forever()

