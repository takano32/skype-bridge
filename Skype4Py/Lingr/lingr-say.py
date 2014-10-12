#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import sys
sys.path.insert(0, '/usr/lib/pymodules/python2.7')
import urllib, urllib2
import cgi

from configobj import ConfigObj
config = ConfigObj("../skype-bridge.conf")
verifier = config['lingr']['verifier']
request = "http://lingr.com/api/room/say?room=%s&bot=%s&text=%s&bot_verifier=%s"
text = urllib.quote_plus('うへー')
request  = request % ('arakawatomonori', 'skype', text, verifier)
print request
response = urllib2.urlopen(request)

