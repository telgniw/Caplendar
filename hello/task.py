#!/usr/bin/env python
# -*- coding: utf8 -*-

from common import *
from db import *

from datetime import *
from google.appengine.api import memcache
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class TaskHandler(webapp.RequestHandler):
    def get(self, what):
        if what == 'clear_old':
            self._clear_old_()
        else:
            self.response.clear()
            self.response.set_status(404)
    def _clear_old_(self):
        bound = datetime.strptime(str(date.today() + timedelta(-7)), '%Y-%m-%d')
        qry = db.Query(Event).filter('time <', bound)
        db.delete_async(qry)

def main():
    run_wsgi_app(webapp.WSGIApplication([
        ('/task/(.*)', TaskHandler)
    ], debug=True))

if __name__ == "__main__":
    main()