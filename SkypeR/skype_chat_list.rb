#! /usr/bin/env ruby
# -*- coding: utf-8 -*-
# Skypeチャットのチャンネル一覧を表示する

require 'rubygems'
require 'Skype'
require 'nkf'

def decode(s)
	NKF.nkf('-Ws', s)
end

Skype.init('SkypeChatList')
Skype.start_messageloop

chats = Skype.searchRecentChats
chats.each do |chat|
	name = decode(chat.getName)
	topic = decode(chat.getTopic)
	puts "#{name} - #{topic}"
	# SkypeAPI::ChatMessage.create(chat.getName, "ほげ")
end

