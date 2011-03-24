#!/usr/bin/env python
# encoding: utf-8

import Skype4Py
import time
import pprint

pp = pprint.PrettyPrinter(indent = 4)

def handler(msg, event):
    if event == u"RECEIVED":
        # print "ChatName %s" % msg.ChatName
        # pp.pprint(msg.Sender.FullName)
        # print ""

        home_chat_name = u'#takano32/$48936a1f975e4866'
        foreign_chat_name = u'#daiy115/$hal_sk;1003c105ba4c04e4'
        foreign_chat_name = u'#masaki.inagi.inoue/$shohei.gree;2b4388279376168e'

        if msg.ChatName == home_chat_name and msg.Sender.Handle == 'takano32':
            skype = Skype4Py.Skype()
            skype.Chat(foreign_chat_name).SendMessage(msg.Body)

        if msg.ChatName == foreign_chat_name:
            print "Handle %s" % msg.Sender.Handle
            print "FullName %s" % msg.Sender.FullName
            pp.pprint(msg.Sender.FullName);
            print "Body %s" % msg.Body
            name = msg.Sender.FullName
            if name == u'':
                name = msg.Sender.Handle
            text = "%s:\n\t%s" % (msg.Sender.FullName, msg.Body)
            skype = Skype4Py.Skype()
            skype.Chat(home_chat_name).SendMessage(text)

        if msg.Body == u"やっぱり":
            msg.Chat.SendMessage(u"猫が好き")

def main():
    skype = Skype4Py.Skype()
    skype.OnMessageStatus = handler
    skype.Attach()
    # イベントハンドラは別スレッドにて実行されるので、
    # 本スレッドではひたすらsleepしてスクリプトが終了しないようにしておく。
    while True:
        time.sleep(1) 

if __name__ == "__main__":
    main()
