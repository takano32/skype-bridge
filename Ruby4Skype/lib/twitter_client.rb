#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
# IRC で作ろうかと思ったけど、セッションの管理などが難しいので
# protected の Twitter で作った方がよさそうだ、などと考えた。

require 'rubygems'
require 'pit'
require 'twitter'
require 'date'

class SimpleTwitterClient
	def initialize(config)
		@config = config
		unless config.has_key?('last_created_at') then
			config['last_created_at'] = Time.now.to_s
		end
		unless config.has_key?('last_reply_created_at') then
			config['last_reply_created_at'] = Time.now.to_s
		end
		
		id = config['twitter_id']
		password = config['twitter_password']
		@twitter = Twitter::Base.new(id, password)
		Pit.set(@config['config_name'], :data => @config)
	end

	def send_message(input)
		@twitter.update(input)
	end

	def receive_message(&block)
		raise unless block_given?
		@message_block = block
	end

	def receive_reply(&block)
		raise unless block_given?
		@reply_block = block
	end

	def start
		@timeline_thread = Thread.start do
			loop do
				update_message
				update_reply
				Pit.set(@config['config_name'], :data => @config)
				sleep(1 * 60 * 3)
			end
		end
	end

	def update_created_at(status, type = '')
		return unless status
		key = "last_#{type.empty? ? '' : type + '_'}created_at"
		last_created_at = Time.parse(@config[key]).localtime
		created_at = Time.parse(status.created_at).localtime
		return unless last_created_at < created_at
		@config[key] = created_at.to_s
		Pit.set(@config['config_name'], :data => @config)
	end
	
	def update_message
		@twitter.timeline.reverse.each do |status|
			update_created_at(status)
			
			user = status.user.screen_name
			id = status.id
			text = status.text.gsub(/&#(\d*?);/) { [$1.to_i].pack('U') }.gsub('&amp;gt;', '>')
			url = "http://twitter.com/#{user}/status/#{id}"

			@message_block.call(user, url, text)
		end
	end

	def update_reply
		last = Time.parse(@config['last_reply_created_at'])
		each_reply_after(last) do |reply|
			update_created_at(status, 'reply')
			@reply_block.call(reply) if @reply_block
		end
	end

	
	
	def each_reply(&block)
		if block_given? then
			@twitter.replies.each do |reply|
				yield reply
			end
		end
	end
	
	def replies_after(time)
		replies = []
		each_reply_after(time) do |reply|
			if time.localtime < Time.parse(reply.created_at) then
				replies << reply
			end
		end
		return replies
	end

	def each_reply_after(time, &block)
		if block_given? then
			each_reply do |reply|
				yield reply if time.localtime < Time.parse(reply.created_at)
			end
		end
	end
	
	def stop
		@timeline_thread.kill
		@timeline_thread.join
	end
end

def twitter_client_sample
	config_name = "TwitterToSkype" + (ARGV[0] ? "-#{ARGV[0]}" : "")
	config = Pit.get(config_name,
			  :require => {
				  'skype_chat' => 'your skype channel id',
				  'skype_name' => 'your skype name',
				  'twitter_id'   => 'bot twitter id',
				  'twitter_password'   => 'bot twitter password',
			  })
	Pit.set(config_name, :data => config.merge({'config_name' => config_name}))
	config = Pit.get(config_name)
	
	stc = SimpleTwitterClient.new(config)
	
	#p stc.replies_after(Time.parse('Fri Feb 27 03:34:41 +0000 2010'))
	#p stc.replies_after(Time.parse('Fri Feb 27 03:34:41 +0000 2009'))
	#p stc.replies_after(Time.parse('Fri Feb 27 03:34:41 +0000 2008'))
	reply = stc.replies_after(Time.parse(config['last_reply_created_at'])).last
	p reply
	stc.update_created_at(reply, 'reply') if reply
	exit

	stc.receive_message do |user, url, message|
		puts '----'
		out = "(talk) @#{user} - #{url} \n #{message}"
		puts out
	end
	
	stc.start

	Signal.trap('INT') do
		stc.stop
		exit
	end

	
	loop do
		Thread.pass
		sleep 0.5
	end


end


def twitter_sample
	t = Twitter::Base.new('hc_skype', 'skype_hc')
	t.timeline.each do |status|
		user = status.user.screen_name
		id = status.id
		text = status.text.gsub(/&#(\d*?);/) { [$1.to_i].pack('U') }
		out = "(talk) @#{user} - http://twitter.com/#{user}/status/#{id} \n #{text}"
		puts '----'
		puts out
		puts DateTime.parse(status.created_at).to_s
	end
	#h = t.user(:hirameki)
	#puts "(talk) http://twitter.com/hirameki/status/#{h.status.id}"
	#puts h.status.text.gsub(/&#(\d*?);/) { [$1.to_i].pack('U') }.gsub('&amp;gt;', '>')
end

if __FILE__ == $0 then
	twitter_client_sample
end
