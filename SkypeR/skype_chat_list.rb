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
Skype.attach_wait

chats = Skype.searchRecentChats
chats.each do |chat|
	name = chat.to_s
	topic = decode(chat.getTopic)
	puts "#{name} - #{topic}"
	# SkypeAPI::ChatMessage.create(chat.getName, "ほげ")
end



