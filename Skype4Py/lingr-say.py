#-*- coding: utf-8 -*-
import urllib, urllib2
import cgi

from configobj import ConfigObj
config = ConfigObj("skype-lingr.conf")
verifier = config['lingr']['verifier']
request = "http://lingr.com/api/room/say?room=%s&bot=%s&text=%s&bot_verifier=%s"
text = urllib.quote_plus('うへー')
request  = request % ('arakawatomonori', 'skype', text, verifier)
print request
response = urllib2.urlopen(request)

