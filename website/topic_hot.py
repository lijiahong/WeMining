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
        form = web.input(type=None,start=None, end=None)
        if not form.start:
            form.start = 0
        if not form.end:
            form.end = time.time()
        query_dict = {}
        query_dict['ts'] = {'$gte': form.start, '$lte': form.end}
        if type:
            query_dict['type'] = type
        return json.dumps(list(db['topics'].find(query_dict, sort=[('ts', pymongo.ASCENDING)])))
