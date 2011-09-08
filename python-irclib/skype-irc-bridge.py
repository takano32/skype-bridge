#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: et sts=4:ts=4:sw=4
# http://d.hatena.ne.jp/nishiohirokazu/20071203/1196670766
#

# /home/takano32/workspace/skype-lingr-bridge/python-irclib/skype-irc-bridge.conf

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
NICKNAME = "skype"
COLOR_TAG = "\x16" #reverse
COLOR_TAG = "\x0310" #aqua

CHANNEL = "#sib"
if sys.argv[1:]:
    CHANNEL = sys.argv[1]

import re
from ircbot import SingleServerIRCBot
from irclib import nm_to_n

class SkypeIRCBridge(SingleServerIRCBot):
	def __init__(self):
        SingleServerIRCBot.__init__(self, [(SERVER, PORT)], NICKNAME, NICKNAME)
		self.channel = CHANNEL

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.join(self.channel)

	def say(self, msg):
		self.connection.privmsg(self.channel, COLOR_TAG + msg)

	def do_command(self, c, e):
		e.nick = nm_to_n(e.source())
		msg = unicode(e.arguments()[0], "utf8")
		self.say(msg.encode('utf-8'))

	on_pubnotice = do_command
	on_privnotice = do_command
	on_pubmsg = do_command
	on_privmsg = do_command

	def skype_handler(msg, event):
		if len(msg.Body) == 0:
			return
		if event == u"RECEIVED":
			config = ConfigObj("skype-lingr.conf")
			for key in config:
				if key == 'lingr' or key == 'skype':
					continue
				if msg.ChatName == config[key]['skype']:
					name = msg.Sender.FullName
				if len(name) == 0 or len(name) > 16:
					name = msg.Sender.Handle
				room = config[key]['lingr']
				verifier = config['lingr']['verifier']
				for line in msg.Body.splitlines():
				    text = '%s: %s' % (name, line)
				    send_message(room, text, verifier)

bot = SkypeIRCBridge()
bot.start()

