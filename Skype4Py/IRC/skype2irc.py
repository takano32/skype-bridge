#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

import sys
import os
import Skype4Py
import pprint
import time
import threading
import xmlrpclib
from configobj import ConfigObj

os.environ['DISPLAY'] = ":16"
os.environ['XAUTHORITY'] = "/home/takano32/.Xauthority"

pp = pprint.PrettyPrinter(indent = 4)

SERVER = "irc.freenode.net"
PORT = 6667
WAIT = None
NICKNAME = "skype"

from ircbot import SingleServerIRCBot
from irclib import nm_to_n

config = ConfigObj("skype-bridge.conf")

if config.has_key('irc') and config['irc'].has_key('server'):
	SERVER = config['irc']['server']

if config.has_key('irc') and config['irc'].has_key('port'):
	PORT = int(config['irc']['port'])

if config.has_key('irc') and config['irc'].has_key('wait'):
	WAIT = float(config['irc']['wait'])

bridge_lock = threading.Lock()

def skype_handler_without_lock(msg, event):
	try:
		skype_handler(msg, event)
	except Skype4Py.errors.ISkypeError, err:
		# print "A fault occurred"
		# print "Fault code: %d" % err.faultCode
		# print "Fault string: %s" % err.faultString
		print "Skype4Py.errors.ISkypeError occured"
		return


def skype_handler(msg, event):
	if len(msg.Body) == 0:
		return
	if event == u"RECEIVED":
		for key in config:
			if key == 'skype' or key == 'irc':
				continue
			if config[key].has_key('skype2irc'):
				if config[key]['skype2irc'].title() == 'False':
					continue
			if config[key].has_key('skype') and msg.ChatName == config[key]['skype']:
				name = msg.Sender.FullName
				if len(name) == 0 or len(name) > 16:
					name = msg.Sender.Handle
				if config[key].has_key('irc'):
					channel = config[key]['irc']
					send_message(channel, name, msg.Body)

def send_message(channel, name, msg):
	lines = msg.splitlines()
	if name.startswith('IRC'):
		return
	if len(lines) == 1 and msg.startswith('@'):
		text = lines[0]
		with bridge_lock:
			bridge.say(channel, text.encode('utf-8'))
		notice = '# %s is issuing the above command.' % name
		with bridge_lock:
			bridge.notice(channel, notice.encode('utf-8'))
		return
	for line in lines:
		texts = list()
		while 150 < len(line):
			text = '%s: %s' % (name, line[:150])
			texts.append(text)
			line = line[149:]
		text = '%s: %s' % (name, line)
		texts.append(text)
		for text in texts:
			with bridge_lock:
				bridge.say(channel, text.encode('utf-8'))
			if WAIT != None:
				time.sleep(WAIT)
			else:
				time.sleep(len(text) / 20.0)

class FromSkypeToIrc(SingleServerIRCBot):
	def __init__(self, server = SERVER):
		SingleServerIRCBot.__init__(self, [(SERVER, PORT)], NICKNAME, NICKNAME)
		self.channel = '#takano32bot'

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


	on_pubnotice = do_command
	on_privnotice = do_command
	on_pubmsg = do_command
	on_privmsg = do_command

skype = Skype4Py.Skype()
skype.OnMessageStatus = skype_handler_without_lock
skype.Attach()
# skype.ClearChatHistory()
# skype.ResetCache()

time.sleep(3)

bridge = FromSkypeToIrc()
bridge.start()

