#-*- coding: utf-8 -*-
require 'sinatra'
require 'json'
require 'open-uri'

def minecraft_time(server_time)
	hours = (((server_time / 1000.0)+8)%24).to_i
	minutes = (((server_time/1000.0)%1)*60).to_i
	seconds = (((((server_time/1000.0)%1)*60)%1)*60).to_i
	"#{hours}:#{minutes}:#{seconds}"
end

post "/lingr/minecraft" do
	begin
		json = JSON.parse(request.body.read)
		break unless json["events"]
		text = []

		json["events"].each do |event|
			next unless event["message"]
			message = event["message"]

			case message["text"]
			when /^(:|\/)minecraft/
				{
				holygrail: "holy-grail.jp",
				futoase: "no32.tk",
				ariela: "ariela.jp"
			}.map{|n,s| [n,s,"http://#{s}:8123/up/world/world/1"] }.each do |server|
				json = JSON.parse(open(server[2]){|io|io.read})
				if json["hasStorm"] || json["isThundering"]
					add = " (#{json["hasStorm"] ? "☂" : ""}#{json["isThundering"] ? "⚡" : ""})"
				else
					add = ""
				end
				text << "[#{server[1]}] #{minecraft_time(json["servertime"])}#{add}"
			end
			end
		end

		text.join("\n")
	rescue Exception => e
		open("/tmp/minecraftbot","w") do |io|
			io.puts e.inspect
			io.puts "--"
			io.puts e.backtrace.join("\n")
		end
	end
end

