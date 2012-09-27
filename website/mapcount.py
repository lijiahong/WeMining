#-*- coding:utf-8 -*-

'''微博话题数量统计
'''

import json
import time
import web
import math
import datetime

import sys
sys.path.append('..')

from tokenizer.fenci import cut
from weibo_search_xapian import WeiboSearch

urls = ('/mapweibo/mapcount', )

class handler():
    def GET(self):
        form = web.input(topic=None, starttime=None, endtime=None)
        topic = form.topic
        starttime = form.starttime
        endtime = form.endtime
        if not topic:
            return json.dumps({'error': 'need a topic'})
        search = WeiboSearch()
        keywords = cut(form.topic)
        whole_count = search.count(keywords=keywords)
        if starttime and endtime:
            begints = timestr2ts(starttime)
            endts = timestr2ts(endtime)
            count = search.count(keywords=keywords, begin=begints, end=endts)
        else:
            count = 0
        return json.dumps({'whole_count': whole_count, 'count': count})

def timestr2ts(timestr):
    result = datetime.datetime.strptime(timestr,"%Y-%m-%d")
    result = time.mktime(result.timetuple())
    return math.floor(float(result))
