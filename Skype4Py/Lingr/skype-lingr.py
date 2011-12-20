#!/usr/bin/env python
# encoding: utf-8
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import Skype4Py
import time
import pprint
import os
import urllib, urllib2
import cgi
from configobj import ConfigObj
from minecraft import Minecraft

pp = pprint.PrettyPrinter(indent = 4)

def send_message(room, text, verifier):
    request = "http://lingr.com/api/room/say?room=%s&bot=%s&text=%s&bot_verifier=%s"
    text = urllib.quote_plus(text.encode('utf-8'))
    request  = request % (room, 'skype', text, verifier)
    response = urllib2.urlopen(request)
    if response.code != 200:
        print 'HTTP Response Code is %d: %s' % (response.code, time.ctime(time.time()))
        time.sleep(3)
        send_message(room, text, verifier)

def handler_with_try(msg, event):
    try:
        handler(msg, event)
    except SkypeAPIError, err:
        print 'Fault time is', time.ctime(time.time())
        time.sleep(5)
        handler(msg, event)

def handler(msg, event):
    if len(msg.Body) == 0:
        return
    if event == u"RECEIVED":
        config = ConfigObj("/home/takano32/workspace/skype-bridge/Skype4Py/skype-bridge.conf")
        for key in config:
            if key == 'lingr' or key == 'skype':
                continue
            if config[key].has_key('skype') and msg.ChatName == config[key]['skype']:
                name = msg.Sender.FullName
                if len(name) == 0 or len(name) > 16:
                    name = msg.Sender.Handle
                room = config[key]['lingr']
                verifier = config['lingr']['verifier']
                for line in msg.Body.splitlines():
                    if name == 'IRC':
                        text = line
                    else:
                        text = '%s: %s' % (name, line)
                    send_message(room, text, verifier)
                    continue # below function is for minecraft
                    if room == 'hametsu_mine' and line == ':minecraft':
                        for status in Minecraft().statuses():
                            text = '%s: %s' % ('minecraft', status)
                            send_message(room, text, verifier)

def bridge():
    skype = Skype4Py.Skype()
    skype.OnMessageStatus = handler_with_try
    skype.Attach()
    for i in range(0, 60 * 5):
        time.sleep(1)
    skype.ResetCache()
    # skype.ClearChatHistory()
    exit()

if __name__ == "__main__":
    bridge()

