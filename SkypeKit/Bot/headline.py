#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

ROOM = "#yuiseki/$4425ae72bc11c305"

import pprint
pp = pprint.PrettyPrinter(indent = 4)

from configobj import ConfigObj
CONFIG = ConfigObj('skype-bridge.conf')

import xmlrpclib
xmlrpc_host = CONFIG['bot']['xmlrpc_host']
xmlrpc_port = CONFIG['bot']['xmlrpc_port']
DAEMON = xmlrpclib.ServerProxy('http://%s:%s' % (xmlrpc_host, xmlrpc_port))

import feedparser
feed = feedparser.parse("http://pipes.yahoo.com/pipes/pipe.run?_id=8f34c1abdb8fc99e9aa057fac8e510e1&_render=rss")

for item in feed['items'][:5]:
	text = item.title + "\n" + item.link
	DAEMON.send_message(ROOM, text)
# for debug
#print pp.pformat(from_lingr)

