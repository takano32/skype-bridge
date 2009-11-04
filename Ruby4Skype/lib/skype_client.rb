#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
# SimpleSkypeClient
# Copyright (c) 2009 TAKANO Mitsuhiro <tak at no32.tk>
#


require 'rubygems'
require 'skype'
require 'thread'

class SimpleSkypeClient
	attr_accessor :messages
	def initialize(chat_id)
		Skype.init('SimpleSkypeClient')
		Skype.start_messageloop
		Skype.attach_wait
		@chat_id = chat_id
		@stop = false
	end

	def send_message(msg)
		Skype::ChatMessage.create(@chat_id, msg)
	end

	def receive_message(&block)
		raise unless block_given?
		@block = block
	end

	def start
		raise unless @block
		Skype::ChatMessage.set_notify :Status, 'RECEIVED' do |msg|
				channel = msg.get_chat.dup
				name = msg.get_from.dup
				message = msg.get_body.dup
				@block.call(channel, name, message)
		end
	end

	def stop
		@stop = true
	end
end


if __FILE__ == $0 then
	priv_chat = 'akio0911'
	test_chat = '#voqn_skype/$6410ca0139e195d0'
	chat = '#akio0911/$yuiseki;1600dfa22ed008f5'
	client = SimpleSkypeClient.new(chat)
	
	client.receive_message do |channel, name, message|
		puts "#{name}: #{message}" if channel == chat
	end
	
	Signal.trap('INT') do
		puts "#{self.class.name}: INT" if $DEBUG
		client.stop
		exit
	end


	client.start

	client.send_message('テスト')

	loop do
		puts "#{self.class.name}: loop" if $DEBUG
		sleep 0.5
	end
	client.stop

end
