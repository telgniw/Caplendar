#!/usr/bin/env python
# -*- coding: utf8 -*-
from google.appengine.ext import db

class Event(db.Model):
    owner = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    time = db.DateTimeProperty(required=True)
    place = db.GeoPtProperty(required=True)
    visibility = db.StringProperty()

class User(db.Model):
    id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
