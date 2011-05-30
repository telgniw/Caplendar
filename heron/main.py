#!/usr/bin/env python
# -*- coding: utf8 -*-
GEOIP_KEY     = '07c5218d90f3894825d40b853a350bd557d5907878bbcd2cfde269ae3d8aebe0'
FB_API_KEY    = '8d955ca9f882c155282c7f3bbbda017c'
FB_APP_ID     = '208577865834024'
FB_APP_SECRET = 'ba90c5d51930b3bfc651d0a1d6819884'
PERMS = 'user_events,create_event,rsvp_event,read_friendlists,manage_friendlists,publish_stream'

import facebook
from db import *
from datetime import *
from django.utils import simplejson
from google.appengine.api import memcache, urlfetch
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
                    user = User(
                        key_name=str(profile['id']), id=str(profile['id']), name=profile['name']
                    )
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
            self._get_menu_()
        elif what == 'event':
            self._get_event_()
        elif what == 'friend':
            self._get_friend_()
        elif what == 'account':
            self._get_account_()
        elif what == 'geopt':
            self._get_geopt_()
        else:
            self.response.clear()
            self.response.set_status(404)
    def post(self, what):
        if what == 'event':
            self._post_event_()
        else:
            self.response.clear()
            self.response.set_status(404)
    def _get_menu_(self):
        self.response.out.write(simplejson.dumps({
            'data': [{
                'name': '行程',
                'qry': 'event'
            }, {
                'name': '好友',
                'qry': 'friend'
            }, {
                'name': '帳號',
                'qry': 'account'
            }],
            'default': 0
        }, ensure_ascii=False))
    def _get_event_(self):
        qry = db.Query(Event).filter('owner =', self.current_user.id)
        empty = True if qry.count(limit=1) == 0 else False
        today, tomorrow = date.today(), date.today() + timedelta(1)
        qry.filter('time >=', datetime(today.year, today.month, today.day))
        qry.filter('time <', datetime(tomorrow.year, tomorrow.month, tomorrow.day))
        events = []
        for event in qry:
            events.append(event)
        output = template.render('event.part.html', {
            'events': events,
            'events_empty': empty
        })
        self.response.out.write(output)
    def _post_event_(self):
        pass
    def _get_friend_(self):
        pass
    def _get_account_(self):
        pass
    def _get_geopt_(self):
        geoip = simplejson.loads(urlfetch.fetch(
            'http://api.ipinfodb.com/v3/ip-city/?key=%s&ip=%s&format=json' % (
                GEOIP_KEY, self.request.remote_addr
            )
        ).content)
        self.response.out.write(simplejson.dumps({
            'data': [
                geoip['latitude'], geoip['longitude']
            ]
        }, ensure_ascii=False))

class EventHandler(BaseHandler):
    def post(self, what):
        if what == 'new':
            self._post_new_()
        elif what == 'delete':
            self._post_delete_()
        else:
            self.response.clear()
            self.response.set_status(404)
    def _post_new_(self):
        event = Event(
            owner = self.current_user.id,
            title = self.request.get('event-name'),
            time = datetime.strptime(self.request.get('event-time'), '%Y/%m/%d %H:%M'),
            place_name = self.request.get('event-place-name'),
            visibility = self.request.get('event-visibility')
        )
        place = self.request.get('event-place')
        if place:
            event.place = GeoPt(place)
        event.put()
        self.redirect('/')
    def _post_delete_(self):
        key = self.request.get('key')
        qry = db.get(key)
        db.delete(qry)

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/', IndexHandler),
        ('/qry/(.*)', QueryHandler),
        ('/event/(.*)', EventHandler)
    ], debug=True))

if __name__ == "__main__":
    main()
