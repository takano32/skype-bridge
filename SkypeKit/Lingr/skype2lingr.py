#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#


from configobj import ConfigObj
from SimpleXMLRPCServer import SimpleXMLRPCServer
import urllib, urllib2
import json
import xml.etree.ElementTree
import lingr

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

CONFIG = ConfigObj("skype-bridge.conf")
ACCOUNT_NAME = CONFIG['lingr']['skype_id']
ACCOUNT_PSW = CONFIG['lingr']['skype_password']
LOGGED_IN = False

class SkypeDaemon():
	def __init__(self):
		global ACCOUNT_NAME, ACCOUNT_PSW
		self.accountName = ACCOUNT_NAME
		self.accountPsw = ACCOUNT_PSW
	
	@staticmethod
	def SendMessage(room, text, verifier):
		request = "http://lingr.com/api/room/say?room=%s&bot=%s&text=%s&bot_verifier=%s"
		text = urllib.quote_plus(text.encode('utf-8'))
		request  = request % (room, 'skype', text, verifier)
		try:
			response = urllib2.urlopen(request)
		except urllib2.HTTPError as err:
			print 'urllib2.HTTPError: %s' % time.ctime(time.time())
			time.sleep(3)
			SkypeDaemon.SendMessage(room, text, verifier)
			return
		if response.code == 200:
			res = json.JSONDecoder().decode(response.read())
			if res.has_key('status'):
				if res['status'] == 'ok':
					return
				else:
					print 'Response status from Lingr: %s' % res['status']
					time.sleep(3)
					SkypeDaemon.SendMessage(room, text, verifier)
			else:
				print 'Response from Lingr dont have status code'
				time.sleep(3)
				SkypeDaemon.SendMessage(room, text, verifier)
		else:
			print 'HTTP Response Code is %d: %s' % (response.code, time.ctime(time.time()))
			time.sleep(3)
			SkypeDaemon.SendMessage(room, text, verifier)
	
	@staticmethod
	def SendMessageWithName(room, name, text, verifier):
		lines = text.splitlines()
		for line in lines:
			if name == 'IRC':
				text = line
			else:
				text = '%s: %s' % (name, line)
			SkypeDaemon.SendMessage(room, text, verifier)

	@staticmethod
	def OnMessage(self, message, changesInboxTimestamp, supersedesHistoryMessage, conversation):
		global CONFIG, ACCOUNT_NAME
		if message.timestamp < time.mktime(time.localtime()) - 300: return
		if message.author == ACCOUNT_NAME: return
		for key in CONFIG:
			if key == 'skype' or key == 'lingr':
					continue
			if CONFIG[key].has_key('skype2lingr'):
				if CONFIG[key]['skype2lingr'].title() == 'False':
					continue
			if not CONFIG[key].has_key('skype'): continue
			if not conversation.identity == CONFIG[key]['skype']: continue
			if CONFIG[key].has_key('lingr'):
				room = CONFIG[key]['lingr']
				verifier = CONFIG['lingr']['verifier']
				name = message.author_displayname
				if len(name) == 0 or len(name) > 16:
					name = message.author

				try:
					elem = xml.etree.ElementTree.fromstring("<body>%s</body>" % message.body_xml.encode('utf-8'))
					text = ""
					for t in elem.itertext():
						text += t
				except Exception as err:
					print message.body_xml.encode('utf-8')
					print err
					text = message.body_xml.encode('utf-8')

				if len(text.splitlines()) == 1 and lingr.room_command(text):
					conversation.PostText('System: bridging w/ http://lingr.com/room/%s' % room)
					return
				print room, text
				SkypeDaemon.SendMessageWithName(room, name, text, verifier)

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
			self.skype = Skype.GetSkype(keypair.keyFileName, port = 8964)
		except Exception:
			raise SystemExit('Unable to create skype instance');
		Skype.Account.OnPropertyChange = self.AccountOnChange
		account = self.skype.GetAccount(self.accountName)
		account.LoginWithPassword(self.accountPsw, False, False)
		print "logging in"
		while LOGGED_IN == False:
			time.sleep(1)
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

if __name__ == "__main__":
	host = CONFIG['lingr']['xmlrpc_host']
	port = CONFIG['lingr']['xmlrpc_port']
	sd = SkypeDaemon()
	sd.login()
	sds = SkypeDaemonServer(sd)
	sv = SimpleXMLRPCServer((host, int(port)))
	sv.register_instance(sds)
	sv.serve_forever()

