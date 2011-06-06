#!/usr/bin/env python
# -*- coding: utf8 -*-

from common import *

from django.utils import simplejson
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class AdminHandler(webapp.RequestHandler):
    def get(self):
        output = template.render('admin/index.html', {
            'app_title': APP_TITLE
        })
        self.response.out.write(output)

class AdminActionHandler(webapp.RequestHandler):
    def post(self, what):
        if what == 'clear_cache':
            self._post_clear_cache_()
        else:
            self.response.clear()
            self.response.set_status(404)
    def _post_clear_cache_(self):
        self.response.out.write(simplejson.dumps({
            'success': memcache.flush_all()
        }, ensure_ascii=False))

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/admin', AdminHandler),
        ('/admin/action/(.*)', AdminActionHandler)
    ], debug=True))

if __name__ == "__main__":
    main()