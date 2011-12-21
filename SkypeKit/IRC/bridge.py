#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
# see also http://d.hatena.ne.jp/nishiohirokazu/20071203/1196670766
#

import sys
import os
import Skype4Py
import time
import pprint
from configobj import ConfigObj

pp = pprint.PrettyPrinter(indent = 4)

SERVER = "irc.freenode.net"
PORT = 6667
WAIT = None
CHANNEL = "#takano32bot"
NICKNAME = "skype"
COLOR_TAG = "\x0310" #aqua
REVERSE_TAG = "\x16" #reverse
NORMAL_TAG = "\x0F" #normal
COLOR_TAG = "" #none


from ircbot import SingleServerIRCBot
from irclib import nm_to_n

config = ConfigObj("skype-irc-bridge.conf")

if config.has_key('irc') and config['irc'].has_key('server'):
	SERVER = config['irc']['server']

if config.has_key('irc') and config['irc'].has_key('port'):
	PORT = int(config['irc']['port'])

if config.has_key('irc') and config['irc'].has_key('wait'):
	WAIT = float(config['irc']['wait'])

def skype_handler(msg, event):
	if len(msg.Body) == 0:
		return
	if event == u"RECEIVED":
		for key in config:
			if key == 'lingr' or key == 'skype' or key == 'irc':
				continue
			if config[key].has_key('skype') and msg.ChatName == config[key]['skype']:
				name = msg.Sender.FullName
				if len(name) == 0 or len(name) > 16:
					name = msg.Sender.Handle
				if config[key].has_key('irc'):
					channel = config[key]['irc']
					for line in msg.Body.splitlines():
						if name == 'Lingr':
							text = line
						else:
							text = '%s: %s' % (name, line)
						bridge.say(channel, text.encode('utf-8'))
						if WAIT != None:
							time.sleep(WAIT)
						else:
							time.sleep(len(text) / 20.0)

class SkypeIRCBridge(SingleServerIRCBot):
	def __init__(self, skype, server = SERVER):
		SingleServerIRCBot.__init__(self, [(SERVER, PORT)], NICKNAME, NICKNAME)
		self.skype = skype
		self.channel = CHANNEL

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.join(self.channel)
		for key in config:
			if key == 'lingr' or key == 'skype' or key == 'irc':
				continue
			if config[key].has_key('irc'):
				channel = config[key]['irc']
				c.join(channel)

	def say(self, channel, msg):
		self.connection.privmsg(channel, COLOR_TAG + msg)

	def do_command(self, c, e):
		msg = unicode(e.arguments()[0], "utf8")
		self.say(self.channel, msg.encode('utf-8'))

	def skype_handler(self, c, e):
		e.nick = nm_to_n(e.source())
		msg = unicode(e.arguments()[0], "utf8")
		text = '%s: %s' % (e.nick, msg)
		for key in config:
			if key == 'lingr' or key == 'skype' or key == 'irc':
				continue
			if config[key].has_key('irc'):
				channel = config[key]['irc']
				if channel == e.target():
					room = self.skype.Chat(config[key]['skype'])
					room.SendMessage(text)

	on_pubnotice = do_command # set skype_handler if catch IRC NOTICE
	on_privnotice = do_command
	on_pubmsg = skype_handler
	on_privmsg = do_command

skype = Skype4Py.Skype()
skype.OnMessageStatus = skype_handler
skype.Attach()

bridge = SkypeIRCBridge(skype)
bridge.start()

