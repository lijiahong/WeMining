#-*- coding:utf-8 -*-

import json
import web
import time
import pymongo

from config import getDB

db = getDB()
urls = ('/api/topic/hot.json', )

class handler():
    def GET(self):
        form = web.input(type=None)
        query_dict = {}
        if type:
            query_dict['type'] = form.type
        return json.dumps(list(db['topics'].find(query_dict, sort=[('ts', pymongo.ASCENDING)])))
