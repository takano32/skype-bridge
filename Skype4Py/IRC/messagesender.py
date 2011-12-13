#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak at no32.tk>
#

from configobj import ConfigObj
import sys, xmlrpclib

CONFIG = ConfigObj("skype-bridge.conf")

xmlrpc_host = CONFIG['skype']['xmlrpc_host']
xmlrpc_port = CONFIG['skype']['xmlrpc_port']
sendmessage = xmlrpclib.ServerProxy('http://%s:%s' % (xmlrpc_host, xmlrpc_port))

room = '#takano32/$mitsuhiro.takano;46c33855977e8974'
sendmessage.send_message(room, 'hogefuga')

