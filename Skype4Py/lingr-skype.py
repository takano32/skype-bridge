import cgi
import json

import pprint
pp = pprint.PrettyPrinter(indent = 4)

import os
import sys

content_length = int(os.environ['CONTENT_LENGTH'])
request_content = sys.stdin.read(content_length)

from_lingr = json.loads(request_content)

print pp.pformat(from_lingr)


