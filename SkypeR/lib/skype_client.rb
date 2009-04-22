#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
# 
# Copyright (c) 2009 TAKANO Mitsuhiro <tak at no32.tk>
#
# http://june29.jp/2008/04/23/ruby4skype/


require 'rubygems'
require 'skypeapi'
require 'thread'

class SimpleSkypeClient
	attr_accessor :messages
	def initialize(chat_id)
		SkypeAPI.init
		SkypeAPI.attachWait
		@chat_id = chat_id
		@stop = false
		@messages = []
	end

	def send_message(msg)
		SkypeAPI::ChatMessage.create(@chat_id, msg)
	end

	def receive_message(&block)
		raise unless block_given?
		@block = block
	end

	def start
		raise unless @block
		SkypeAPI::ChatMessage.setNotify :Status, 'RECEIVED' do |msg|
			@messages.push(msg)
		end
		@thread = Thread.start do
			until (@stop)
				puts "#{self.class.name}: polling" if $DEBUG
				SkypeAPI.polling
				Thread.pass
				sleep 0.56789
				while (msg = @messages.pop) do
					channel = msg.getChat.dup
					name = msg.getFrom.dup
					message = msg.getBody.dup
					@block.call(channel, name, message)
				end
			end
		end
	end

	def stop
		@stop = true
		@thread.join
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
		Thread.pass
		sleep 0.5
	end
	client.stop

end
