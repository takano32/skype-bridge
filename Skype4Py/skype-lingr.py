#!/usr/bin/env python
# encoding: utf-8

import Skype4Py
import time
import pprint
import os
import urllib, urllib2
import cgi
from configobj import ConfigObj


os.environ['DISPLAY'] = ":32"
os.environ['XAUTHORITY'] = "/var/www/.Xauthority"
pp = pprint.PrettyPrinter(indent = 4)

def send_message(room, text, verifier):
    request = "http://lingr.com/api/room/say?room=%s&bot=%s&text=%s&bot_verifier=%s"
    text = urllib.quote_plus(text.encode('utf-8'))
    request  = request % (room, 'skype', text, verifier)
    response = urllib2.urlopen(request)

def handler(msg, event):
    if event == u"RECEIVED":
        config = ConfigObj("skype-lingr.conf")
        for key in config:
            if key == 'lingr' or key == 'skype':
                continue
            if msg.ChatName == config[key]['skype']:
                name = msg.Sender.FullName
                if len(name) == 0:
                    name = msg.Sender.Handle
		if config[key].has_key('skype.prefix'):
                	prefix = config[key]['skype.prefix']
		else:
			prefix = ""
                text = "%s%s: %s" % (prefix, name, msg.Body)
                verifier = config['lingr']['verifier']
                send_message(config[key]['lingr'], text, verifier)

def bridge():
    skype = Skype4Py.Skype()
    skype.OnMessageStatus = handler
    skype.Attach()
    while True:
        time.sleep(1)

def main():
    bridge()

if __name__ == "__main__":
    main()

