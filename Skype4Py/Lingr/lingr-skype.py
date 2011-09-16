#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import sys
sys.path.append('/usr/lib/pymodules/python2.5')
sys.path.append('/usr/lib/pymodules/python2.5/gtk-2.0')

import os
os.environ['DISPLAY'] = ":16"
os.environ['XAUTHORITY'] = "/var/www/.Xauthority"

import cgi
import json
import time
import re

import pprint
pp = pprint.PrettyPrinter(indent = 4)

import Skype4Py

from configobj import ConfigObj
# config_path = os.path.join(os.path.dirname(sys.argv[0]), 'skype-lingr.conf')
# config_path = os.path.join(os.path.dirname(os.environ['SCRIPT_FILENAME']), 'skype-lingr.conf')
config_path = '/home/takano32/workspace/skype-bridge/Skype4Py/skype-bridge.conf'
config = ConfigObj(config_path)

if not os.environ.has_key('CONTENT_LENGTH'):
    exit()

content_length = int(os.environ['CONTENT_LENGTH'])
request_content = sys.stdin.read(content_length)

from_lingr = json.JSONDecoder().decode(request_content)

print "Content-Type: text/plain"
print

if not from_lingr.has_key('events'):
    print
    exit()

def handler(msg, event):
    pass

def send_message(room, text):
    room.SendMessage(text)

skype = Skype4Py.Skype()
skype.OnMessageStatus = handler
skype.Attach()

for event in from_lingr['events']:
    if not event.has_key('message'):
        continue
    for key in config:
        if key == 'lingr' or key == 'skype' or key == 'irc':
            continue
        if not config[key].has_key('lingr'):
            continue
        if not config[key].has_key('skype'):
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
skype.ResetCache()
time.sleep(1.5)
print
exit()
# for debug
#print pp.pformat(from_lingr)

