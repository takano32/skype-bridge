#!/usr/bin/env python
# encoding: utf-8

import Skype4Py
import time
import pprint

pp = pprint.PrettyPrinter(indent = 4)

def handler(msg, event):
    if event == u"RECEIVED":
        # pp.pprint(msg.Sender.FullName)
        # print ""
        test_chat_name = u'#takano32/$1e1c02f5b9a8de94'
        # merge_chat_name = u'#masaki.inagi.inoue/$masaki.fujimoto;2060dfac7d8a8f27'
        merge_chat_name = test_chat_name
        if msg.ChatName == merge_chat_name:
            print "ChatName %s" % msg.ChatName
            print "Body %s" % msg.Body

def merge_bot():
    skype = Skype4Py.Skype()
    skype.OnMessageStatus = handler
    skype.Attach()
    while True:
        time.sleep(1)

class MergeList:
    pass

def main():
    merge = new MergeList()
    merge.merge('hoge')

if __name__ == "__main__":
    # merge_bot()
    main()

