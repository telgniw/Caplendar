#!/usr/bin/env python
# -*- coding: utf8 -*-

from db import *
from base import *

from datetime import *
from django.utils import simplejson
from google.appengine.api.datastore_types import GeoPt
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class EventHandler(BaseHandler):
    def get(self, what):
        if what == 'list':
            self._get_list_()
        else:
            self.response.clear()
            self.response.set_status(404)
    def _get_list_(self):
        id = self.request.get('id')
        if id:
            qry = db.Query(Event).filter('owner =', id).filter('visibility', 'public')
        else:
            qry = db.Query(Event).filter('owner =', self.current_user.id)
        empty, events = (qry.count(limit=1) == 0), []
        if not empty:
            today = datetime.strptime(self.request.get('time'), '%Y-%m-%d')
            tomorrow = today + timedelta(1)
            qry.filter('time >=', today).filter('time <', tomorrow)
            for event in qry:
                events.append(to_dict(event))
        self.response.out.write(simplejson.dumps({
            'empty': empty,
            'data': {
                'num': len(events),
                'events': events
            }
        }, ensure_ascii=False))
    def post(self, what):
        if what == 'new_or_edit':
            self._post_new_or_edit_()
        elif what == 'delete':
            self._post_delete_()
        elif what == 'share':
            self._post_share_()
        else:
            self.response.clear()
            self.response.set_status(404)
    def _post_new_or_edit_(self):
        status, key = True, self.request.get('event-key')
        event = db.get(key) if key else Event(owner=self.current_user.id)
        try:
            event.title, event.time, event.place_name, event.visibility = (
                self.request.get('event-name'),
                datetime.strptime(self.request.get('event-time'), '%Y-%m-%d %H:%M'),
                self.request.get('event-place-name'),
                self.request.get('event-visibility')
            )
            place = self.request.get('event-place')
            if place:
                event.place = GeoPt(self.request.get('event-place'))
        except (ValueError, db.BadValueError):
            status = False
        if not status:
            self.response.clear()
            self.response.set_status(400)
        else:
            event.put()
            self.response.out.write(simplejson.dumps({
                'data': {
                    'key': event.key_str()
                }
            }, ensure_ascii=False))
    def _post_delete_(self):
        key = self.request.get('key')
        event = db.get(key)
        db.delete(event)
        self.response.out.write(simplejson.dumps({
            'data': {
                'key': key
            }
        }, ensure_ascii=False))
    def _post_share_(self):
        key = self.request.get('key')
        event = db.get(key)
        event.fb_event_id = self.request.get('fb-event-id')
        event.put()
        self.response.out.write(simplejson.dumps({
            'data': {
                'key': key
            }
        }, ensure_ascii=False))