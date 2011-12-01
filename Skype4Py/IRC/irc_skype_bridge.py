#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak at no32.tk>
#

from ircbot import SingleServerIRCBot
from irclib import nm_to_n
from configobj import ConfigObj
from SimpleXMLRPCServer import SimpleXMLRPCServer

import sys, xmlrpclib

CONFIG = ConfigObj("bridge.conf")
SERVER = 'irc.freenode.net'
PORT = 6667
NICKNAME = 'skype2'

class IrcSkypeBridge(SingleServerIRCBot):
	def __init__(self, server = SERVER):
		self.channel = '#takano32bot'
		SingleServerIRCBot.__init__(self, [(SERVER, PORT)], NICKNAME, NICKNAME)

		xmlrpc_host = CONFIG['skype']['xmlrpc_host']
		xmlrpc_port = CONFIG['skype']['xmlrpc_port']
		self.skype = xmlrpclib.ServerProxy('http://%s:%s' % (xmlrpc_host, xmlrpc_port))

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

	def say(self, channel, msg):
		self.connection.privmsg(channel, msg)
		return True

	def do_command(self, c, e):
		msg = unicode(e.arguments()[0], "utf8")
		self.say(self.channel, msg.encode('utf-8'))

	def handler(self, c, e):
		e.nick = nm_to_n(e.source())
		msg = unicode(e.arguments()[0], "utf8")
		text = '%s: %s' % (e.nick, msg)
		for key in CONFIG:
			if key == 'skype' or key == 'irc':
				continue
			if CONFIG[key].has_key('irc'):
				channel = CONFIG[key]['irc']
				if channel == e.target():
					self.skype.say(CONFIG[key]['skype'], text)

	on_pubnotice = do_command
	on_privnotice = do_command
	on_pubmsg = handler
	on_privmsg = do_command

if __name__ == "__main__":
	host = CONFIG['irc']['xmlrpc_host']
	port = CONFIG['irc']['xmlrpc_port']
	sv = SimpleXMLRPCServer((host, int(port)))
	bridge = IrcSkypeBridge()
	bridge.start()
	sv.register_instance(bridge)
	sv.serve_forever()

