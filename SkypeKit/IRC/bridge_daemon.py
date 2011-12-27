#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#


from configobj import ConfigObj
from SimpleXMLRPCServer import SimpleXMLRPCServer

# START using SkypeKit
import sys
import keypair
from time import sleep

sys.path.append(keypair.distroRoot + '/ipc/python');
sys.path.append(keypair.distroRoot + '/interfaces/skype/python');
try:
	import Skype;
except ImportError:
    raise SystemExit('Program requires Skype and skypekit modules');
# END using SkypeKit

CONFIG = ConfigObj("skype-bridge.conf")
ACCOUNT_NAME = CONFIG['irc']['skype_id']
ACCOUNT_PSW = CONFIG['irc']['skype_password']
LOGGED_IN = False

import Queue
IRC_MESSAGES = Queue.Queue()

class SkypeDaemon():
	def __init__(self):
		global ACCOUNT_NAME, ACCOUNT_PSW
		self.accountName = ACCOUNT_NAME
		self.accountPsw = ACCOUNT_PSW

	@staticmethod
	def OnMessage(self, message, changesInboxTimestamp, supersedesHistoryMessage, conversation):
		global CONFIG
		global ACCOUNT_NAME
		if message.author != ACCOUNT_NAME:
			for key in CONFIG:
				if key == 'skype' or key == 'irc':
						continue
				if CONFIG[key].has_key('skype2irc'):
						if CONFIG[key]['skype2irc'].title() == 'False':
								continue
				if CONFIG[key].has_key('skype') and conversation.identity == CONFIG[key]['skype']:
						if CONFIG[key].has_key('irc'):
								channel = CONFIG[key]['irc']
								nick = message.author_displayname
								text = message.body_xml
								global IRC_MESSAGES
								print channel, text
								IRC_MESSAGES.put((channel, nick, text))

	@staticmethod
	def AccountOnChange(self, property_name):
		print self.status
		if property_name == 'status' and self.status == 'LOGGED_IN':
			global ACCOUNT_NAME
			print "Logging in with", ACCOUNT_NAME
			global LOGGED_IN
			LOGGED_IN = True

	def login(self):
		global LOGGED_IN
		LOGGED_IN = False
		Skype.Skype.OnMessage = self.OnMessage;
		try:
			self.skype = Skype.GetSkype(keypair.keyFileName);
		except Exception:
			raise SystemExit('Unable to create skype instance');
		Skype.Account.OnPropertyChange = self.AccountOnChange
		account = self.skype.GetAccount(self.accountName)
		account.LoginWithPassword(self.accountPsw, False, False)
		print "logging in"
		while LOGGED_IN == False:
			sleep(1)
		print "logged in"

	def stop(self):
		self.skype.stop()

class SkypeDaemonServer():
	def __init__(self, skype):
		self.skype = skype

	def send_message(self, room, msg):
		conv = self.skype.skype.GetConversationByIdentity(room)
		conv.PostText(msg, False)
		return True

	def pop_message(self):
		global IRC_MESSAGES
		try:
			message = IRC_MESSAGES.get_nowait()
		except Queue.Empty as err:
			message = False
		return message

	def re_attach(self):
		self.skype.login()
		return True

if __name__ == "__main__":
	host = CONFIG['irc']['xmlrpc_host']
	port = CONFIG['irc']['xmlrpc_port']
	sd = SkypeDaemon()
	sd.login()
	sds = SkypeDaemonServer(sd)
	sv = SimpleXMLRPCServer((host, int(port)))
	sv.register_instance(sds)
	sv.serve_forever()

