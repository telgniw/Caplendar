#!/usr/bin/env python
# -*- coding: utf8 -*-
GEOIP_KEY     = '07c5218d90f3894825d40b853a350bd557d5907878bbcd2cfde269ae3d8aebe0'

from base import *

from django.utils import simplejson
from google.appengine.api import memcache, urlfetch
from google.appengine.ext.webapp import template
import pickle

class QueryHandler(BaseHandler):
    def get(self, what):
        if what == 'geopt':
            self._get_geopt_()
        elif what == 'friend':
            self._get_friend_()
        else:
            self.response.clear()
            self.response.set_status(404)
    def _get_geopt_(self):
        geoip = memcache.get(self.request.remote_addr)
        if geoip:
            geoip = pickle.loads(geoip)
        else:
            try:
                geoip = simplejson.loads(urlfetch.fetch(
                    'http://api.ipinfodb.com/v3/ip-city/?key=%s&ip=%s&format=json' % (
                        GEOIP_KEY, self.request.remote_addr
                    )
                ).content)
            except urlfetch.DownloadError:
                geoip = { 'latitude': 23.5, 'longitude': 121.5 }
            memcache.set(self.request.remote_addr, pickle.dumps(geoip), time=604800)
        self.response.out.write(simplejson.dumps({
            'data': {
                'geoip': geoip
            }
        }, ensure_ascii=False))
    def _get_friend_(self):
        cache_key, graph = self.current_user.id, facebook.GraphAPI(self.cookie['access_token'])
        cache, fb = memcache.get(cache_key), graph.get_connections('me', 'friends')['data']
        if cache:
            friends = pickle.loads(cache)
            for user in fb:
                if user['id'] in friends:
                    continue
                if User.get_by_key_name(user['id']):
                    friends.append(user)
        else:
            friends = []
            for user in fb:
                if User.get_by_key_name(user['id']):
                    friends.append(user)
        memcache.set(cache_key, pickle.dumps(friends), time=604800)
        self.response.out.write(simplejson.dumps({
            'data': {
                'num': len(friends),
                'friends': friends
            }
        }, ensure_ascii=False))