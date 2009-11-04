#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
# 
# Copyright (c) 2009 TAKANO Mitsuhiro <tak at no32.tk>
#
# tsbot.rb: Twitter Skype Bot
#

require 'pit'
require 'twitter_client'
require 'skype_client'

class TwitterSkypeBot
	@@reply = nil
	def initialize(config)
		@config = config
		@skype_chat = config['skype_chat']
		@skype_name = config['skype_name']
		@skype_client = SimpleSkypeClient.new(@skype_chat)
		@twitter_client = SimpleTwitterClient.new(config)
		skype_initialize
		@skype_client.start
		twitter_initialize
		@twitter_client.start
	end

	# post question to skype
	def twitter_initialize
=begin
		@twitter_client.receive_message do |user, url, message|
			out = " (talk) @#{user} - #{url} \n #{message} "
			@skype_client.send_message(out)
		end
=end
		last = Time.parse('0').localtime
		if @config.has_key?('last_reply_created_at') then
			last = Time.parse(@config['last_reply_created_at']).localtime
		end
		reply = @twitter_client.replies_after(last).last
		@twitter_client.update_created_at(reply, 'reply')
		return unless reply
			
		text = reply.text.gsub(/&#(\d*?);/) { [$1.to_i].pack('U') }
		name = reply.user.screen_name
		out = " (call) here comes a new tweet from @#{name} ..." 
		@skype_client.send_message(out)
		sleep 8
		out = " (call) #{text} "
		@skype_client.send_message(out)
		@@reply = reply
	end

	# receive answer from skype
	def skype_initialize
		@skype_client.receive_message do |channel, name, message|
			if @@reply and @skype_chat == channel.to_s then
				name = @@reply.user.screen_name
				out = "@#{name} #{message} - by 86"
				@twitter_client = SimpleTwitterClient.new(@config)
				@twitter_client.send_message(out)
				@twitter_client.update_created_at(@@reply, 'reply')
				@@reply = nil
			end
		end
	end

	
	def start
		# start when initialize
	end

	def stop
		@twitter_client.stop
		@skype_client.stop
	end	
end


if __FILE__ == $0 then
	config_name = "TwitterSkypeBot" + (ARGV[0] ? "-#{ARGV[0]}" : "")
	config = Pit.get(config_name,
						  :require => {
							  'skype_chat' => 'your skype channel id',
							  'skype_name' => 'your skype name',
							  'twitter_id'   => 'bot twitter id',
							  'twitter_password'   => 'bot twitter password',
						  })
	Pit.set(config_name, :data => config.merge({'config_name' => config_name}))
	config = Pit.get(config_name)


	bot = TwitterSkypeBot.new(config)
	bot.start

	Signal.trap('INT') do
		bot.stop
		exit
	end
	
	(10 * 180).times do
		Thread.pass
		sleep 0.1
	end
end

