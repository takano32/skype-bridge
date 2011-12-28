#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import sys
import os
import json
import re

import pprint
pp = pprint.PrettyPrinter(indent = 4)

from configobj import ConfigObj
config = ConfigObj('/home/takano32/workspace/skype-bridge/SkypeKit/skype-bridge.conf')

import xmlrpclib
xmlrpc_host = config['lingr']['xmlrpc_host']
xmlrpc_port = config['lingr']['xmlrpc_port']
skype_daemon = xmlrpclib.ServerProxy('http://%s:%s' % (xmlrpc_host, xmlrpc_port))

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
            for line in text.splitlines():
                msg = '%s: %s' % (name, line)
                skype_daemon.send_message(room, msg)
print
exit()
# for debug
#print pp.pformat(from_lingr)

