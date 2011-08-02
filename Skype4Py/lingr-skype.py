#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import sys
sys.path.append('/usr/lib/pymodules/python2.5')
sys.path.append('/usr/lib/pymodules/python2.5/gtk-2.0')

import cgi
import json

import pprint
pp = pprint.PrettyPrinter(indent = 4)

import os
import re
import time

os.environ['DISPLAY'] = ":32"
os.environ['XAUTHORITY'] = "/var/www/.Xauthority"

import Skype4Py

from configobj import ConfigObj
config = ConfigObj("/home/takano32/workspace/skype-lingr-bridge/Skype4Py/skype-lingr.conf")

content_length = int(os.environ['CONTENT_LENGTH'])
request_content = sys.stdin.read(content_length)

from_lingr = json.JSONDecoder().decode(request_content)

print "Content-Type: text/plain"
print

def handler(msg, event):
    pass

def send_message(room, text):
    room.SendMessage(text)

skype = Skype4Py.Skype()
skype.OnMessageStatus = handler
skype.Attach()

for event in from_lingr['events']:
    for key in config:
        if key == 'lingr' or key == 'skype':
            continue
        if event['message']['room'] == config[key]['lingr']:
            text = event['message']['text']
            name = event['message']['nickname']
            if re.compile(u'荒.*?川.*?智.*?則').match(name):
                name = event['message']['speaker_id']
            if len(name) > 16:
                name = event['message']['speaker_id']
            room = config[key]['skype']
            room = skype.Chat(room)
            for line in text.splitlines():
                msg = '%s: %s' % (name, line)
                send_message(room, msg)
    print

exit()

# for debug
#print pp.pformat(from_lingr)

