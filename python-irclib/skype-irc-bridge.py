#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# http://d.hatena.ne.jp/nishiohirokazu/20071203/1196670766
#

import sys
SERVER = "irc.freenode.net"
PORT = 6667
NICKNAME = "skype"
COLOR_TAG = "\x16" #reverse
COLOR_TAG = "\x0310" #aqua

CHANNEL = "#sib"
if sys.argv[1:]:
    CHANNEL = sys.argv[1]

import re
from ircbot import SingleServerIRCBot
from irclib import nm_to_n

class SkypeIRCBridge(SingleServerIRCBot):
    def __init__(self):
        SingleServerIRCBot.__init__(self, [(SERVER, PORT)], NICKNAME, NICKNAME)
        self.channel = CHANNEL

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def say(self, msg):
        self.connection.privmsg(self.channel, COLOR_TAG + msg)

    def do_command(self, c, e):
        e.nick = nm_to_n(e.source())
        msg = unicode(e.arguments()[0], "utf8")
        self.say(msg.encode('utf-8'))

    on_pubnotice = do_command
    on_privnotice = do_command
    on_pubmsg = do_command
    on_privmsg = do_command

bot = SkypeIRCBridge()
bot.start()

