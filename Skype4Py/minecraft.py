#!/usr/bin/env python
# encoding: utf-8
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import urllib2
import json
import math

class Minecraft():
    def __init__(self):
        self.servers = dict()
        self.servers[u'HolyGrail'] = u'holy-grail.jp'
        self.servers[u'futoase'] = u'192.168.32.10'
        self.servers[u'ariela']  = u'ariela.jp'

    def time(self, server_time):
        hours = math.floor((((server_time / 1000.0)+8)%24))
        minutes = math.floor((((server_time/1000.0)%1)*60))
        seconds = math.floor((((((server_time/1000.0)%1)*60)%1)*60))
        return u"%02d:%02d:%02d" % (hours, minutes, seconds)

    def status(self, server_name, server_addr):
        response = urllib2.urlopen(u'http://%s:8123/up/world/world/1' % server_addr).read()
        data = json.JSONDecoder().decode(response)
        weather = u'☀'
        if data[u'hasStorm']:
            weather = u'☂'
        elif data[u'isThundering']:
            weather = u'⚡'
        time = self.time(data[u'servertime'])
        return u"%-16s [%s] %s" % (server_name, time, weather)

    def statuses(self):
        result = []
        for name, addr in self.servers.items():
           result.append(self.status(name, addr))
        return result
            

        
if __name__ == '__main__':
    m = Minecraft()
    print m.statuses()

