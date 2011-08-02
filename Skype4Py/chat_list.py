#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# encoding: utf-8

import Skype4Py
import time
import pprint
import os

os.environ['DISPLAY'] = ":32"
pp = pprint.PrettyPrinter(indent = 4)

def handler(msg, event):
    if event == u"RECEIVED":
        # pp.pprint(msg.Sender.FullName)
        # print ""
        print "ChatName %s" % msg.ChatName
        print "Body %s" % msg.Body
        print ""

def chat_list():
    skype = Skype4Py.Skype()
    skype.OnMessageStatus = handler
    skype.Attach()
    while True:
        time.sleep(1)

class MergeList:
    pass

def main():
    chat_list()

if __name__ == "__main__":
    # merge_bot()
    main()

