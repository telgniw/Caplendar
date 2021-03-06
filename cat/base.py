#!/usr/bin/env python
# -*- coding: utf8 -*-

PERMS = 'user_events,create_event,rsvp_event,publish_stream'

from common import *
from db import *
import facebook

from google.appengine.api import memcache
from google.appengine.ext import webapp

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
                    user = User(
                        key_name=str(profile['id']), id=str(profile['id']), name=profile['name']
                    )
                    user.put()
                memcache.set(user.id, cookie['access_token'], time=86400)
                self._current_user = user
        return self._current_user