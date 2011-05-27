#!/usr/bin/env python
# -*- coding: utf8 -*-
FB_API_KEY    = '8d955ca9f882c155282c7f3bbbda017c'
FB_APP_ID     = '208577865834024'
FB_APP_SECRET = 'ba90c5d51930b3bfc651d0a1d6819884'
PERMS = 'user_events,create_event,rsvp_event,read_friendlists,manage_friendlists,publish_stream'

import facebook
from db import *
from datetime import *
from django.utils import simplejson
from google.appengine.api import memcache
from google.appengine.api.datastore_types import GeoPt
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class BaseHandler(webapp.RequestHandler):
    @property
    def current_user(self):
        if not hasattr(self, '_current_user'):
            self._current_user = None
            cookie = facebook.get_user_from_cookie(self.request.cookies, FB_APP_ID, FB_APP_SECRET)
            if cookie:
                user = User.get_by_key_name(cookie['uid'])
                if not user:
                    graph = facebook.GraphAPI(cookie['access_token'])
                    profile = graph.get_object('me')
                    user = User(key_name=str(profile['id']),
                                id=str(profile['id']),
                                name=profile['name'])
                    user.put()
                memcache.set(user.id, cookie['access_token'])
                self._current_user = user
        return self._current_user
    
class IndexHandler(BaseHandler):
    def get(self):
        output = template.render('index.html', {
            'current_user': self.current_user,
            'fb_api_key': FB_API_KEY,
            'fb_app_id': FB_APP_ID,
            'perms': PERMS
        })
        self.response.out.write(output)

class QueryHandler(BaseHandler):
    def get(self, what):
        if what == 'menu':
            self.response.out.write(simplejson.dumps({
                'data': [{
                    'name': '行程',
                    'qry': 'event'
                }, {
                    'name': '帳號',
                    'qry': 'account'
                }],
                'default': 0
            }, ensure_ascii=False))
        elif what == 'event':
            pass
        else:
            self.response.out.write('{}')

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/', IndexHandler),
        ('/qry/(.*)', QueryHandler),
    ], debug=True))

if __name__ == "__main__":
    main()
