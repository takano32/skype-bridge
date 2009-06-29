#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
# 
# Copyright (c) 2009 TAKANO Mitsuhiro <tak at no32.tk>
#
# sig.rb: SkypeIrcGateway
# 建設予定地
#

require 'pit'
require '../lib/irc_client'
require '../lib/skype_client'

class SkypeIrcGateway
	def initialize(config)
		@skype_chat = config['skype_chat']
		@skype_name = config['skype_name']
		@irc_chat = config['irc_chat']
		@irc_name = config['irc_name']
		@skype_client = SimpleSkypeClient.new(@skype_chat)
		@irc_client = SimpleIrcClient.new(@irc_chat, @irc_name)
		skype_initialize
		irc_initialize
	end
	
	def skype_initialize
		@skype_client.receive_message do |channel, name, message|
			message.each_line do |msg|
				break unless @skype_chat == channel.to_s
				if @prev_irc_name == name.to_s then
					@irc_client.send_message(msg)
				else
					@prev_irc_name = name.to_s
					@irc_client.send_message(" > #{name} < ")
					@irc_client.send_message(msg)
				end
			end
		end
	end

	def irc_initialize
		@irc_client.receive_message do |channel, name, message|
			if @prev_skype_name == name then
				msg = " > #{message}"
			else
				@prev_skype_name = name
				msg = "(swear) #{name}\n > #{message}"
			end
			@skype_client.send_message(msg) if @irc_chat == channel
		end
	end

	def start
		@skype_client.start
		@irc_client.start
	end

	def stop
		@skype_client.stop
		@irc_client.stop
	end	
end


if __FILE__ == $0 then
	config = Pit.get("SkypeIrcGateway" + (ARGV[0] ? "-#{ARGV[0]}" : ""),
						  :require => {
							  'skype_chat' => 'your skype channel id',
							  'skype_name' => 'your skype name',
							  'irc_chat'   => 'bot irc channel',
							  'irc_name'   => 'bot irc name',
						  })

	gw = SkypeIrcGateway.new(config)
	gw.start

	Signal.trap('INT') do
		gw.stop
		exit
	end
	
	loop do
		Thread.pass
		sleep 0.5
	end
end

