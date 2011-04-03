#! /usr/bin/env python
import cgi
import json

import pprint
pp = pprint.PrettyPrinter(indent = 4)

import os
import sys

content_length = int(os.environ['CONTENT_LENGTH'])
request_content = sys.stdin.read(content_length)

from_lingr = json.JsonReader().read(request_content)

print "Content-Type: text/plain"
print

#for event in from_lingr['events']:
#	print event['message']['text']
# (swear)






# for debug
#print pp.pformat(from_lingr)
