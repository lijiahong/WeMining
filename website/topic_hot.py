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
        form = web.input(type=None, start=None, end=None)
        query_dict = {}
        if form.type:
            query_dict['type'] = form.type
        start = form.start
        end = form.end
        if not start:
            start = 0
        else:
            start = int(start)
        if not end:
            end = int(time.time())
        else:
            end = int(end)
        query_dict['ts'] = {'$gte': start, '$lte': end}
        results = []
        try:
            r = db['topics'].find(query_dict, sort=[('ts', pymongo.ASCENDING)])
        except:
            return json.dumps({'error': 'something wrong.'})
        for r in :
            results.append({'topic': r['topic'],
                            'count': r['count'],
                            'ts': r['ts'],
                            'type': r['type']})
        return json.dumps(results)
