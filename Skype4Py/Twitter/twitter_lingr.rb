#!/usr/bin/env ruby
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak at no32.tk>
#

require 'rubygems'
require 'pit'
require 'oauth'
require 'rubytter'


require 'open-uri'
def say(text)
	v = Digest::SHA1.hexdigest("tweet"+"RVuGW2N01hAUcHMwpQOsBey5zol")
	url = "http://lingr.com/api/room/say?room=takano32&bot=tweet&text=#{text}&bot_verifier=#{v}"
	open(url)
end

config = Pit.get("twitter",
		  :require => {
			  'consumer_key' => 'client CONSUMER_KEY',
			  'consumer_secret' => 'client CONSUMER_SECRET',
			  'access_token' => 'oauth ACCESS_TOKEN',
			  'access_token_secret' => 'oauth ACCESS_TOKEN_SERCTET',
	  })
CONSUMER_KEY = config['consumer_key']
CONSUMER_SECRET = config['consumer_secret']
ACCESS_TOKEN = config['access_token']
ACCESS_TOKEN_SECRET = config['access_token_secret']

consumer = OAuth::Consumer.new(
  CONSUMER_KEY,
  CONSUMER_SECRET,
  :site => 'http://api.twitter.com'
)

access_token = OAuth::AccessToken.new(
  consumer,
  ACCESS_TOKEN,
  ACCESS_TOKEN_SECRET
)

client = OAuthRubytter.new(access_token)

last_id = 0
loop do
	begin
		client.list_statuses('takano32', 'my-timeline').reverse.each do |status|
			next unless last_id < status[:id]
			nick = status[:user][:screen_name]
			tweet = status[:text]
			say URI.encode("#{nick}: #{tweet}")
			last_id = status[:id]
		end
	rescue
		retry
	ensure
		sleep 40
	end
end

