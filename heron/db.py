#!/usr/bin/env python
# -*- coding: utf8 -*-
from google.appengine.ext import db

class Event(db.Model):
    owner = db.StringProperty(required=True)
    title = db.StringProperty()
    time = db.DateTimeProperty()
    end_time = db.DateTimeProperty()
    place = db.GeoPtProperty()
    place_name = db.StringProperty()
    visibility = db.StringProperty()

class User(db.Model):
    id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
