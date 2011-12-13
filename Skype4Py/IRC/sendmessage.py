#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak at no32.tk>
#

import Skype4Py
from configobj import ConfigObj
from SimpleXMLRPCServer import SimpleXMLRPCServer
import threading
import os

os.environ['DISPLAY'] = ":16"
os.environ['XAUTHORITY'] = "/home/takano32/.Xauthority"

CONFIG = ConfigObj("skype-bridge.conf")

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

if __name__ == "__main__":
	host = CONFIG['skype']['xmlrpc_host']
	port = CONFIG['skype']['xmlrpc_port']
	sv = SimpleXMLRPCServer((host, int(port)))
	sv.register_instance(SendMessage())
	sv.serve_forever()

