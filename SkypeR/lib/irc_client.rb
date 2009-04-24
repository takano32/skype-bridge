#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
# http://d.hatena.ne.jp/curi1119/20080506/1210062892
# 
# Copyright (c) 2009 TAKANO Mitsuhiro <tak at no32.tk>
#
# SkypeIrcGatewayのために作成したIRCクライアント
require 'socket'
require 'thread'

class SimpleIrcClient
	def initialize(channel, name)
		@server = "irc.freenode.net"
		@port = 6667
		@irc = TCPSocket.new(@server, @port)
		@eol = "\r\n"
		@channel = channel
		@name = name
		@mutex = Mutex.new
	end
	
	def send_cmd(cmd)
		@mutex.synchronize do
			p "Sending command..... :#{cmd}" if $DEBUG
			s = cmd[0...510] + @eol
			@irc.write(s)
			sleep 0.6 # prevent Excess Flood
		end
	end

	def send_message(input)
		send_cmd("PRIVMSG #{@channel} :#{input}")
	end

	def receive_message(&block)
		raise unless block_given?
		@block = block
	end

	def login_and_join
		send_cmd("USER #{@name}, #{@server}, ignore, Hacker's Cafe")
		send_cmd("NICK #{@name}")
		send_cmd("JOIN #{@channel}")
	end

	def start
		@read_thread = read_thread = Thread.start do
			while msg = @irc.gets.split
				p msg.join(' ') if $DEBUG
				send_cmd("PONG #{msg[1]}") if msg[0] == 'PING'
				if msg[1] == 'PRIVMSG' then
					raise unless @block
					channel = msg[2]
					/^:([^!]*)!/ =~ msg[0]
					name = $1
					message = msg[3..-1].join(' ')[1..-1]
					@block.call(channel, name, message)
				end
			end
		end
		login_and_join
	end

	def stop
		@read_thread.join
	end
end


if __FILE__ == $0 then
	channel = '#hackerscafe'
	name = '_32skype'
	client = SimpleIrcClient.new(channel, name)
	client.receive_message do |channel, name, message|
		puts("(swear) #{name}:  #{message}") unless channel == name
	end
	client.start
	client.send_message('hoge fuga')
	client.stop
end

