#-*- coding:utf-8 -*-

import json
import time
import pymongo

from config import getDB

db = getDB()
urls = ('/api/topic/now.json', )

class handler():
    def GET(self):
        hour_topics = [[x['topic'], x['count']] for x in db['topics'].find({'type': 'hour'}, sort=[('ts', pymongo.DESCENDING)]).limit(10)]
        day_topics = [[x['topic'], x['count']] for x in db['topics'].find({'type': 'day'}, sort=[('ts', pymongo.DESCENDING)]).limit(10)]
        week_topics = [[x['topic'], x['count']] for x in db['topics'].find({'type': 'week'}, sort=[('ts', pymongo.DESCENDING)]).limit(10)]
        return json.dumps({'hourly': hour_topics, 'daily': day_topics, 'weekly': week_topics})
