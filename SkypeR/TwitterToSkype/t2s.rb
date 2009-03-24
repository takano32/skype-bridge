#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
# 
# Copyright (c) 2009 TAKANO Mitsuhiro <tak at no32.tk>
#
# t2s.rb: TwitterToSkype
# TwitterのメッセージをSkypeチャットに流します
#

require 'pit'
require 'twitter_client'
require 'skype_client'

class TwitterToSkype
	def initialize(config)
		@skype_chat = config['skype_chat']
		@skype_name = config['skype_name']
		@skype_client = SimpleSkypeClient.new(@skype_chat)
		@twitter_client = SimpleTwitterClient.new(config)
		skype_initialize
		twitter_initialize
	end

	def skype_initialize
		@skype_client.receive_message do |channel, name, message|
		end
	end
	
	def twitter_initialize
		@twitter_client.receive_message do |user, url, message|
			#out = '-' * 30
			out = " (talk) @#{user} - #{url} \n #{message} "
			#out += '-' * 30
			@skype_client.send_message(out)
		end
	end
	
	def start
		@skype_client.start
		@twitter_client.start
	end

	def stop
		@skype_client.stop
		@twitter_client.stop
	end	
end


if __FILE__ == $0 then
	config = Pit.get("TwitterToSkype" + (ARGV[0] ? "-#{ARGV[0]}" : ""),
						  :require => {
							  'skype_chat' => 'your skype channel id',
							  'skype_name' => 'your skype name',
							  'twitter_id'   => 'bot twitter id',
							  'twitter_password'   => 'bot twitter password',
						  })

	gw = TwitterToSkype.new(config)
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

