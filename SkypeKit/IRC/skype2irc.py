#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

import sys
import os
import pprint
import time
import random
import threading
import xmlrpclib
from configobj import ConfigObj
import xml.etree.ElementTree

pp = pprint.PrettyPrinter(indent = 4)

SERVER = "irc.freenode.net"
PORT = 6667
WAIT = None
NICKNAME = "skype"

from ircbot import SingleServerIRCBot
from irclib import nm_to_n

CONFIG = ConfigObj("skype-bridge.conf")

if CONFIG.has_key('irc') and CONFIG['irc'].has_key('server'):
	SERVER = CONFIG['irc']['server']

if CONFIG.has_key('irc') and CONFIG['irc'].has_key('port'):
	PORT = int(CONFIG['irc']['port'])

if CONFIG.has_key('irc') and CONFIG['irc'].has_key('wait'):
	WAIT = float(CONFIG['irc']['wait'])

class Skype2IRC(SingleServerIRCBot):
	def __init__(self, server = SERVER):
		SingleServerIRCBot.__init__(self, [(SERVER, PORT)], NICKNAME, NICKNAME)
		xmlrpc_host = CONFIG['irc']['xmlrpc_host']
		xmlrpc_port = CONFIG['irc']['xmlrpc_port']
		self.daemon = xmlrpclib.ServerProxy('http://%s:%s' % (xmlrpc_host, xmlrpc_port))
		self.channel = "#takano32bot"

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.join(self.channel)
		for key in CONFIG:
			if key == 'skype' or key == 'irc':
				continue
			if CONFIG[key].has_key('irc'):
				channel = CONFIG[key]['irc']
				c.join(channel)
		self.timer_handler()

	def timer_handler(self):
		try:
			message = self.daemon.pop_message()
		except xml.parsers.expat.ExpatError, err:
			message = False
		if message != False:
			(channel, nick, body_xml) = message
			print time.ctime(time.time()), ': ', channel
			elem = xml.etree.ElementTree.fromstring("<body>%s</body>" % body_xml.encode('utf-8'))
			text = ""
			for t in elem.itertext():
				text += t
			lines = text.splitlines()
			if len(lines) == 1 and text.startswith('@'):
				text = lines[0]
				self.say(channel, text.encode('utf-8'))
				notice = '# %s is issuing the above command.' % nick
				self.notice(channel, notice.encode('utf-8'))
			else:
				for line in lines:
					texts = list()
					while 150 < len(line):
						text = '%s: %s' % (nick, line[:150])
						texts.append(text)
						line = line[149:]
					text = '%s: %s' % (nick, line)
					texts.append(text)
					for text in texts:
						self.say(channel, text.encode('utf-8'))
						if WAIT != None:
							time.sleep(WAIT)
						else:
							time.sleep(len(text) / 20.0)
			t = threading.Timer(0.1, self.timer_handler)
			t.start()
		else:
			time.sleep(1)
			t = threading.Timer(1.0, self.timer_handler)
			t.start()

	def say(self, channel, msg):
		self.connection.privmsg(channel, msg)

	def notice(self, channel, msg):
		self.connection.notice(channel, msg)

	def do_command(self, c, e):
		try:
			msg = unicode(e.arguments()[0], "utf8")
			self.say(self.channel, msg.encode('utf-8'))
		except UnicodeDecodeError, err:
			print "UnicodeDecodeError occured"
			return

	on_pubnotice = do_command
	on_privnotice = do_command
	on_pubmsg = do_command
	on_privmsg = do_command

bridge = Skype2IRC()
bridge.start()

