#-*- coding:utf-8 -*-

import json
import web
import re

import sys
sys.path.append('..')

from config import getDB
from spider.queues import MidQueue

db = getDB()
urls = ('/api/topic/push.json', )
job_list = MidQueue()

class handler():
    def GET(self):
        form = web.input(mid=None, info=None)
        mid = form.mid
        info = form.info
        if not mid or not info:
            return json.dumps({'error': 'wrong argmuents need both mid and its info.'})
        if not re.search(r'([a-z]|[A-Z]|[0-9])+', mid):
            return json.dumps({'error': 'wrong mid format,need some like "ykBUBdjEm"'})
        try:
            job_list.push(mid, info)
            return json.dumps({'status': 'ok'})
        except:
            return json.dumps({'error': 'something wrong in push to queue.'})
        return json.dumps(results)
