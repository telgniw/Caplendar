#!/usr/bin/env python
# -*- coding: utf8 -*-

from common import *
from db import *

from django.utils import simplejson
from google.appengine.api import memcache
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class AdminHandler(webapp.RequestHandler):
    def get(self):
        output = template.render('admin/index.html', {
            'app_title': APP_TITLE,
            'fb_api_key': FB_API_KEY,
            'fb_app_id': FB_APP_ID
        })
        self.response.out.write(output)

class AdminActionHandler(webapp.RequestHandler):
    def post(self, what):
        if what == 'flush_cache':
            self._post_flush_cache_()
        elif what == 'list_user':
            self._post_list_user_()
        else:
            self.response.clear()
            self.response.set_status(404)
    def _post_flush_cache_(self):
        self.response.out.write(simplejson.dumps({
            'success': memcache.flush_all()
        }, ensure_ascii=False))
    def _post_list_user_(self):
        offset, num = self.request.get('offset'), self.request.get('num')
        qry = db.Query(User, keys_only=True)
        empty, users = (qry.count(limit=1) == 0), []
        if not empty:
            users = qry.fetch(int(num), int(offset))
        self.response.out.write(simplejson.dumps({
            'empty': empty,
            'data': {
                'num': len(users),
                'users': [u.name() for u in users]
            }
        }, ensure_ascii=False))

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/admin/', AdminHandler),
        ('/admin/action/(.*)', AdminActionHandler)
    ], debug=True))

if __name__ == "__main__":
    main()