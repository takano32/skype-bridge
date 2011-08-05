#!/usr/bin/env python
# encoding: utf-8
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import urllib2
import json
import math

class Minecraft():
    def time(self, server_time):
        hours = math.floor((((server_time / 1000.0)+8)%24))
        minutes = math.floor((((server_time/1000.0)%1)*60))
        seconds = math.floor((((((server_time/1000.0)%1)*60)%1)*60))
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def status(self, server_name):
        response = urllib2.urlopen('http://%s:8123/up/world/world/1' % server_name).read()
        data = json.JSONDecoder().decode(response)
        weather = '☀'
        if data['hasStorm']:
            weather = '☂'
        elif data['isThundering']:
            weather = '⚡'
        time = self.time(data['servertime'])
        return "%s [%s] %s" % (server_name, time, weather)
        
if __name__ == '__main__':
    m = Minecraft()
    print m.status('no32.tk')

