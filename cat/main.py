#!/usr/bin/env python
# -*- coding: utf8 -*-

from db import *
from base import *
from event import *
from query import *

from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
    
class IndexHandler(BaseHandler):
    def get(self):
        output = template.render('index.html', {
            'current_user': self.current_user,
            'fb_api_key': FB_API_KEY,
            'fb_app_id': FB_APP_ID,
            'perms': PERMS
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
