#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
# vim: noet sts=4:ts=4:sw=4
# author: takano32 <tak at no32.tk>
#
# 1.0 - All of idea and essential logic are simply stolen from http://gyazo.com
# 1.1 - Fixed a bug of using same title for every images.
# 1.2 - Stole an idea of allowing an user to specify "Title" and cancel uploading from iLoveGyazickr.app at http://www.sofa.ne.jp/iLoveGazickr-0.1.dmg. And fix some bugs.
# 1.3 - Fixed a bug that QuickLook may not be invoked expectedly.
# 
require 'net/http'
require 'digest/md5'
require 'rexml/document'
require 'open-uri'

require 'rubygems'
require 'pit'

class Frick
	CONTENT_TYPE = 2
	HOST = 'api.flickr.com'
	CGI = '/services/upload/'
	ENV['HOME'] = '/home/takano32'
	def initialize(url)
		@uri = URI.parse(url)
		config = Pit.get("flickr",
				 :require => {
			'api_key' => 'flickr api_key',
			'secret' => 'flickr secret',
			'frob' => 'flickr frob',
			'auth_token' => 'flickr auth_token',
		})

		@api_key = config['api_key'].force_encoding('UTF-8')
		@secret = config['secret'].force_encoding('UTF-8')
		@frob = config['frob'].force_encoding('UTF-8')
		@auth_token = config['auth_token'].force_encoding('UTF-8')
	end

	def post(title)
		id = Time.new.strftime("%Y%m%d%H%M%S")
		imagedata = open(@uri).read
		boundary = '----BOUNDARYBOUNDARY----'.encode('UTF-8')
		api_sig = Digest::MD5.hexdigest("#{@secret}api_key#{@api_key}auth_token#{@auth_token}content_type#{CONTENT_TYPE}title#{title}")
data = <<EOF
--#{boundary}\r
content-disposition: form-data; name="api_key"\r
\r
#{@api_key}\r
--#{boundary}\r
content-disposition: form-data; name="auth_token"\r
\r
#{@auth_token}\r
--#{boundary}\r
content-disposition: form-data; name="api_sig"\r
\r
#{api_sig}\r
--#{boundary}\r
content-disposition: form-data; name="content_type"\r
\r
#{CONTENT_TYPE}\r
--#{boundary}\r
content-disposition: form-data; name="title"\r
\r
#{title}\r
--#{boundary}\r
content-disposition: form-data; name="photo"; filename="#{id}"\r
content-type: image/png
\r
#{imagedata.force_encoding('UTF-8')}\r
\r
--#{boundary}--\r
EOF

		header ={
			'Content-Length' => data.length.to_s,
			'Content-type' => "multipart/form-data; boundary=#{boundary}"
		}

		Net::HTTP.start(HOST,80) do |http|
			res = http.post(CGI,data,header)
			if res.body.match(/<photoid>(.*)<\/photoid>/) then
				photo_id = $1

				method = 'flickr.photos.getInfo'
				api_sig = Digest::MD5.hexdigest("#{@secret}api_key#{@api_key}method#{method}photo_id#{photo_id}")
				res = http.get("/services/rest/?method=#{method}&api_key=#{@api_key}&photo_id=#{photo_id}&api_sig=#{api_sig}")

				doc = REXML::Document.new res.body
				photo = doc.root.elements['photo']
				id = photo.attributes['id']
				secret = photo.attributes['secret']
				server = photo.attributes['server']
				farm = photo.attributes['farm']

				# url = "http://farm#{farm}.static.flickr.com/#{server}/#{id}_#{secret}.jpg"
				# http://www.flickr.com/photos/takano32/6481097191/in/photostream
				url = "http://www.flickr.com/photos/takano32/#{id}/in/photostream"
				return url
			end
		end
	end
end


if $0 == __FILE__ then
	fvl = Frick.new('http://cache.gyazo.com/519d713363838e3910e79f0b9445e128.png')
	puts fvl.post('bar')
end

