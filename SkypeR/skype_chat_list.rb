#! /usr/bin/env ruby
# -*- coding: utf-8 -*-
# Skypeチャットのチャンネル一覧を表示する

require 'rubygems'
require 'skypeapi'
require 'nkf'

def decode(s)
	NKF.nkf('-Ws', s)
end

SkypeAPI.init
SkypeAPI.attachWait

chats = SkypeAPI::searchRecentChats
chats.each do |chat|
	name = decode(chat.getName)
	topic = decode(chat.getTopic)
	puts "#{name} - #{topic}"
	# SkypeAPI::ChatMessage.create(chat.getName, "ほげ")
end

