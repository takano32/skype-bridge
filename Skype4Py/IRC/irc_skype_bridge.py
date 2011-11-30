#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak at no32.tk>
#

import sys, xmlrpclib

def main():
	peer = xmlrpclib.ServerProxy('http://' + sys.argv[1])
	s = raw_input('>>')
	while s:
		room = u"hogefugafoooooo"
		peer.say(room, unicode(s))
		s = raw_input('>>')

if __name__ == "__main__":
	main()

