#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#


from configobj import ConfigObj

# START using SkypeKit
import sys
import keypair
import time

sys.path.append(keypair.distroRoot + '/ipc/python');
sys.path.append(keypair.distroRoot + '/interfaces/skype/python');
try:
	import Skype;
except ImportError:
	raise SystemExit('Program requires Skype and skypekit modules');
# END using SkypeKit

CONFIG = ConfigObj("../skype-bridge.conf")
ACCOUNT_NAME = CONFIG['bot']['skype_id']
ACCOUNT_PSW = CONFIG['bot']['skype_password']
LOGGED_IN = False

class SkypeDaemon():
	def __init__(self):
		global ACCOUNT_NAME, ACCOUNT_PSW
		self.accountName = ACCOUNT_NAME
		self.accountPsw = ACCOUNT_PSW

	@staticmethod
	def OnMessage(self, message, changesInboxTimestamp, supersedesHistoryMessage, conversation):
		pass

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
			self.skype = Skype.GetSkype(keypair.keyFileName, port = 8963)
			self.skype.Start()
		except Exception:
			raise SystemExit('Unable to create skype instance');
		Skype.Account.OnPropertyChange = self.AccountOnChange
		account = self.skype.GetAccount(self.accountName)
		account.LoginWithPassword(self.accountPsw, False, False)
		print "logging in..."
		while LOGGED_IN == False:
			time.sleep(1)
		print "login successfully."

	def stop(self):
		self.skype.stop()

	def send_message(self, room, msg):
		conv = self.skype.GetConversationByIdentity(room)
		conv.PostText(msg, False)
		return True

from SimpleXMLRPCServer import SimpleXMLRPCServer

if __name__ == "__main__":
	host = CONFIG['bot']['xmlrpc_host']
	port = CONFIG['bot']['xmlrpc_port']
	sd = SkypeDaemon()
	sd.login()
	sv = SimpleXMLRPCServer((host, int(port)))
	sv.register_instance(sd)
	sv.serve_forever()

