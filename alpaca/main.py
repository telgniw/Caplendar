#!/usr/bin/env python
GOOGLE_API_KEY      = 'ABQIAAAABzhqZwKt-c2lUjTZzDws8hTu24iuO4IwvTOXPnVFH2VJ8ve_XBRB52Rf40Le-W-WU8MNLHZQKUMdew'
FACEBOOK_API_KEY    = '8d955ca9f882c155282c7f3bbbda017c'
FACEBOOK_APP_ID     = '208577865834024'
FACEBOOK_APP_SECRET = 'ba90c5d51930b3bfc651d0a1d6819884'
PERMISSION = 'user_events,create_event,rsvp_event'

import facebook
from datetime import *
from google.appengine.api.datastore_types import GeoPt
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Event(db.Model):
    title = db.StringProperty(required=True)
    time = db.DateTimeProperty(required=True)
    place = db.GeoPtProperty(required=True)

class User(db.Model):
    id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)

class BaseHandler(webapp.RequestHandler):
    @property
    def current_user(self):
        if not hasattr(self, "_current_user"):
            self._current_user = None
            cookie = facebook.get_user_from_cookie(
                self.request.cookies, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
            )
            if cookie:
                user = User.get_by_key_name(cookie["uid"])
                if not user:
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = User(key_name=str(profile["id"]),
                                id=str(profile["id"]),
                                name=profile["name"],
                                access_token=cookie["access_token"])
                    user.put()
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                self._current_user = user
        return self._current_user
    
class HomeHandler(BaseHandler):
    def get(self):
        output = template.render('index.html', {
            'current_user': self.current_user,
            'google_api_key' : GOOGLE_API_KEY,
            'facebook_api_key': FACEBOOK_API_KEY,
            'facebook_app_id': FACEBOOK_APP_ID,
            'permission': PERMISSION,
            'calendar': [
                Event(key_name="event-00", title='blah-00', time=datetime.now(), place=GeoPt(24.800000, 121.500000)),
                Event(key_name="event-01", title='blah-01', time=datetime.now(), place=GeoPt(25.040000, 121.520000)),
                Event(key_name="event-02", title='blah-02', time=datetime.now(), place=GeoPt(25.080000, 121.510000)),
                Event(key_name="event-03", title='blah-03', time=datetime.now(), place=GeoPt(25.030000, 121.540000)),
                Event(key_name="event-04", title='blah-04', time=datetime.now(), place=GeoPt(24.860000, 121.400000)),
                Event(key_name="event-05", title='blah-05', time=datetime.now(), place=GeoPt(24.820000, 121.000000)),
                Event(key_name="event-06", title='blah-06', time=datetime.now(), place=GeoPt(24.960000, 121.360000)),
                Event(key_name="event-07", title='blah-07', time=datetime.now(), place=GeoPt(25.080000, 121.280000)),
                Event(key_name="event-08", title='blah-08', time=datetime.now(), place=GeoPt(25.200000, 121.540000)),
                Event(key_name="event-09", title='blah-09', time=datetime.now(), place=GeoPt(25.020000, 121.360000)),
                Event(key_name="event-10", title='blah-10', time=datetime.now(), place=GeoPt(24.900000, 121.480000)),
                Event(key_name="event-11", title='blah-11', time=datetime.now(), place=GeoPt(24.720000, 121.240000)),
                Event(key_name="event-12", title='blah-12', time=datetime.now(), place=GeoPt(25.000000, 121.180000)),
                Event(key_name="event-13", title='blah-13', time=datetime.now(), place=GeoPt(25.240000, 121.600000)),
                Event(key_name="event-14", title='blah-14', time=datetime.now(), place=GeoPt(25.120000, 121.440000)),
                Event(key_name="event-15", title='blah-15', time=datetime.now(), place=GeoPt(24.660000, 121.480000)),
                Event(key_name="event-16", title='blah-15', time=datetime.now(), place=GeoPt(25.020000, 121.540000)),
                Event(key_name="event-17", title='blah-16', time=datetime.now(), place=GeoPt(25.000000, 121.500000))
            ]
        })
        self.response.out.write(output)

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ("/.*", HomeHandler)
    ], debug=True))

if __name__ == "__main__":
    main()
