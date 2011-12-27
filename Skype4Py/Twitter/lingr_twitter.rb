#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak@no32 dot tk>
#

ENV['HOME'] = '/home/takano32'
ENV['GEM_HOME'] = ENV['HOME'] + '/.gem'

require 'rubygems'
require 'pit'
require 'oauth'
require 'rubytter'

require 'json'

require ENV['HOME'] + '/workspace/skype-bridge/Skype4Py/Twitter/frick'

puts "Content-Type: text/plain"
puts ""

tweets = []
from_lingr = JSON.parse(ARGF.read.force_encoding('UTF-8'))
from_lingr["events"].each do |event|
	if event["message"] then
		tweets << event["message"]["text"]
	end
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

hashtags = %w(
putya
)
hashtag = ([''] + hashtags).join(' #')
hashtag = ""

tweets.each do |tweet|
	# client.update(tweet + ' ')
	if File.exists?('/tmp/gyazo') then
		gyazo = %x(cat /tmp/gyazo)
		url = Frick.new(gyazo.chomp).post(tweet)
		client.update("#{tweet} #{url} #{hashtag}")
		File.delete('/tmp/gyazo')
	else
		if tweet =~ %r!^http://gyazo.! then
			%x(echo '#{tweet.sub(%r!//gyazo!, "//cache.gyazo").sub(%r!(\.png)?$!, '.png')}' > /tmp/gyazo)
		else
			client.update(tweet + hashtag)
		end
	end
end

