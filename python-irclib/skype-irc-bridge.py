#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# http://d.hatena.ne.jp/nishiohirokazu/20071203/1196670766
#

import sys
sys.path.append('/usr/lib/pymodules/python2.5')
sys.path.append('/usr/lib/pymodules/python2.5/gtk-2.0')
import os
import Skype4Py
import time
import pprint
from configobj import ConfigObj

os.environ['DISPLAY'] = ":32"
os.environ['XAUTHORITY'] = "/var/www/.Xauthority"
pp = pprint.PrettyPrinter(indent = 4)

SERVER = "irc.freenode.net"
PORT = 6667
CHANNEL = "#takano32bot"
NICKNAME = "skype"
COLOR_TAG = "\x0310" #aqua
COLOR_TAG = "\x16" #reverse
COLOR_TAG = "" #none

from ircbot import SingleServerIRCBot
from irclib import nm_to_n

config = ConfigObj("skype-irc-bridge.conf")

def skype_handler(msg, event):
	if len(msg.Body) == 0:
		return
	if event == u"RECEIVED":
		for key in config:
			if key == 'lingr' or key == 'skype' or key == 'irc':
				continue
			if msg.ChatName == config[key]['skype']:
				name = msg.Sender.FullName
				if len(name) == 0 or len(name) > 16:
					name = msg.Sender.Handle
				if config[key].has_key('irc'):
					channel = config[key]['irc']
					for line in msg.Body.splitlines():
						text = '%s: %s' % (name, line)
						bot.say(channel, text.encode('utf-8'))
						time.sleep(len(text) / 20.0)

class SkypeIRCBridge(SingleServerIRCBot):
	def __init__(self, skype, room, channel = CHANNEL, server = SERVER):
		SingleServerIRCBot.__init__(self, [(SERVER, PORT)], NICKNAME, NICKNAME)
		self.skype = skype
		self.room = room
		self.channel = channel

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.join(self.channel)

	def say(self, channel, msg):
		self.connection.privmsg(channel, COLOR_TAG + msg)

	def do_command(self, c, e):
		msg = unicode(e.arguments()[0], "utf8")
		self.say(self.channel, msg.encode('utf-8'))

	def skype_handler(self, c, e):
		e.nick = nm_to_n(e.source())
		msg = unicode(e.arguments()[0], "utf8")
		text = '%s: %s' % (e.nick, msg)
		room = self.skype.Chat(self.room)
		room.SendMessage(text)

	on_pubnotice = do_command
	on_privnotice = do_command
	on_pubmsg = skype_handler
	on_privmsg = do_command

skype = Skype4Py.Skype()
skype.OnMessageStatus = skype_handler
skype.Attach()

for key in config:
	if key == 'lingr' or key == 'skype' or key == 'irc':
		continue
	if config[key].has_key('irc'):
		channel = config[key]['irc']
		room = config[key]['skype']
		bot = SkypeIRCBridge(skype, room, channel)
		bot.start()

