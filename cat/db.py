#!/usr/bin/env python
# -*- coding: utf8 -*-
from datetime import *
from google.appengine.api.datastore_types import GeoPt
from google.appengine.ext import db

def to_dict(model):
    dic = { 'key': model.key_str() }
    for key, prop in model.properties().iteritems():
        val = getattr(model, key)
        if val is None:
            continue
        elif isinstance(val, datetime):
            dic[key] = val.strftime('%Y/%m/%d %H:%M')
        elif isinstance(val, GeoPt):
            dic[key] = {'latitude': val.lat, 'longitude': val.lon}
        else:
            dic[key] = val
    return dic

class BaseModel(db.Model):
    def key_str(self):
        return str(self.key())

class Event(BaseModel):
    owner = db.StringProperty(required=True)
    title = db.StringProperty()
    time = db.DateTimeProperty()
    end_time = db.DateTimeProperty()
    place = db.GeoPtProperty()
    place_name = db.StringProperty()
    visibility = db.StringProperty()

class User(BaseModel):
    id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
