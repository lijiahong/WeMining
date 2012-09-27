# -*- coding: utf-8 -*-

import json
import time
import web

import sys
sys.path.append('..')

from tokenizer.fenci import cut
from weibo_search_xapian import WeiboSearch

urls = ('/mapweibo/trendnum', )

def date2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

def unix2local(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

class handler():
    def GET(self):
        form = web.input(topic=None)
        topic = form.topic
        if topic:
            return topic_dist(topic)
        else:
            return json.dumps({'error': 'need a topic.'})

def topic_dist(topic):
    begin = 0
    end = int(time.time())
    search = WeiboSearch()
    results = search.spread_query(begin=begin, end=end, keywords=cut(topic))
    finals = []
    ts_count = {}
    for status in results:
        ts = date2ts(unix2local(status['timestamp']))*1000
        if ts not in ts_count:
            ts_count[ts] = 0
        ts_count[ts] += 1
    ts_count = sorted(ts_count.iteritems(), key=lambda(k, v): k)
    return json.dumps(ts_count)

if __name__ == '__main__':
    print topic_dist(u'钓鱼岛')
