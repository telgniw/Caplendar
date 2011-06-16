#!/usr/bin/env python
# -*- coding: utf8 -*-

from common import *
from db import *
from base import *
from event import *
from query import *

from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import urllib, urlparse
    
class IndexHandler(BaseHandler):
    def get(self):
        access_token = memcache.get(self.current_user.id) if self.current_user else None
        output = template.render('index.html', {
            'app_title': APP_TITLE,
            'current_user': self.current_user,
            'fb_api_key': FB_API_KEY,
            'fb_app_id': FB_APP_ID,
            'login_url': 'https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=%s' % (
                FB_APP_ID, urllib.quote(urlparse.urljoin(self.request.url, '/app')), PERMS
            )
        })
        self.response.out.write(output)

class AppHandler(BaseHandler):
    def get(self):
        if self.current_user:
            access_token = memcache.get(self.current_user.id)
            output = template.render('app.html', {
                'app_title': APP_TITLE,
                'current_user': self.current_user,
                'access_token': access_token,
                'fb_api_key': FB_API_KEY,
                'fb_app_id': FB_APP_ID
            })
            self.response.out.write(output)
        else:
            self.redirect('/')


class TabHandler(BaseHandler):
    def post(self):
        output = template.render('tab.html', {
            'app_title': APP_TITLE
        })
        self.response.out.write(output)

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/', IndexHandler),
        ('/app', AppHandler),
        ('/tab/', TabHandler),
        ('/qry/(.*)', QueryHandler),
        ('/event/(.*)', EventHandler)
    ], debug=True))

if __name__ == "__main__":
    main()
