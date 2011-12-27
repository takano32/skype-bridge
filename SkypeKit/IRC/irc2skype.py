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
import re

pp = pprint.PrettyPrinter(indent = 4)

SERVER = "irc.freenode.net"
PORT = 6667
WAIT = None
NICKNAME = "to_skype"

from ircbot import SingleServerIRCBot
from irclib import nm_to_n

config = ConfigObj("skype-bridge.conf")

if config.has_key('irc') and config['irc'].has_key('server'):
	SERVER = config['irc']['server']

if config.has_key('irc') and config['irc'].has_key('port'):
	PORT = int(config['irc']['port'])

if config.has_key('irc') and config['irc'].has_key('wait'):
	WAIT = float(config['irc']['wait'])

class IRC2Skype(SingleServerIRCBot):
	def __init__(self, server = SERVER):
		SingleServerIRCBot.__init__(self, [(SERVER, PORT)], NICKNAME, NICKNAME)
		xmlrpc_host = config['irc']['xmlrpc_host']
		xmlrpc_port = config['irc']['xmlrpc_port']
		self.skype = xmlrpclib.ServerProxy('http://%s:%s' % (xmlrpc_host, xmlrpc_port))
		self.channel = "#takano32bot"

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.join(self.channel)
		for key in config:
			if key == 'skype' or key == 'irc':
				continue
			if config[key].has_key('irc'):
				channel = config[key]['irc']
				c.join(channel)

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

	def skype_handler_for_pubmsg(self, c, e):
		return self.skype_handler(c, e, True)

	def skype_handler_for_pubnotice(self, c, e):
		return self.skype_handler(c, e, True)

	def skype_handler(self, c, e, notice = False):
		nick = e.nick = nm_to_n(e.source())
		if nick.startswith(u'skype') or re.compile(u'S_*').match(nick): return
		try:
			msg = unicode(e.arguments()[0], "utf8")
		except UnicodeDecodeError, err:
			print "UnicodeDecodeError occured"
			return
		for key in config:
			if key == 'skype' or key == 'irc':
				continue
			if config[key].has_key('irc2skype'):
				if config[key]['irc2skype'].title() == 'False':
					continue
			if config[key].has_key('irc'):
				channel = config[key]['irc']
				if channel == e.target():
					room = config[key]['skype']
					print time.ctime(time.time()), ': ', channel
					self.send_message(room, nick, msg, notice)

	def send_message(self, room, nick, msg, notice = False):
		try:
			if not notice and msg.startswith(u'@'):
				self.skype.send_message(room, msg)
				notice = '# %s is issuing the above command.' % nick
				self.skype.send_message(room, notice)
				return
			text = '%s: %s' % (nick, msg)
			self.skype.send_message(room, text)
		except xmlrpclib.Fault, err:
			print "A fault occurred"
			print "Fault code: %d" % err.faultCode
			print "Fault string: %s" % err.faultString
			#print "Skype4Py.errors.ISkypeError"
			print 'Fault time: ', time.ctime(time.time())
			pp.pprint(room)
			pp.pprint(text)
			self.skype.re_attach()
			time.sleep(random.random() * 10)
			self.send_message(room, nick, msg, notice)

	on_pubnotice = skype_handler_for_pubnotice
	on_privnotice = do_command
	on_pubmsg = skype_handler_for_pubmsg
	on_privmsg = do_command

bridge = IRC2Skype()
bridge.start()

