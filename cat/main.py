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
    
class IndexHandler(BaseHandler):
    def get(self):
        access_token = memcache.get(self.current_user.id) if self.current_user else None
        output = template.render('index.html', {
            'current_user': self.current_user,
            'fb_api_key': FB_API_KEY,
            'fb_app_id': FB_APP_ID,
            'perms': PERMS,
            'app_title': APP_TITLE,
            'access_token': access_token
        })
        self.response.out.write(output)

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/', IndexHandler),
        ('/qry/(.*)', QueryHandler),
        ('/event/(.*)', EventHandler)
    ], debug=True))

if __name__ == "__main__":
    main()
