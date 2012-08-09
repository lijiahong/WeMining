#-*- coding:utf-8 -*-

import json
import web
import redis
import sys

from config import getDB

db = getDB()
r = redis.Redis()

topic_suggest_key = 'topic:suggest'
topic_hot_key = 'topic:hot'

urls = ('/api/topic/suggest.json', )

class handler():
    def GET(self):
        form = web.input(tag=None)
        q = form.tag
        if not q:
            return json.dumps({'error': 'no topic'})
        return json.dumps(suggest(q))

def suggest(q, count=10):
    results = []
    rangelen = 10
    start = r.zrank(topic_suggest_key, q)
    if not start:
        return results
    while len(results) < count:
        _range = r.zrange(topic_suggest_key, start, start+rangelen-1)
        start += rangelen
        if not _range:
            break
        for prefix in _range:
            if not prefix.startswith(q.encode('utf-8')):
                break
            if prefix[-1] == '*':
                results.append(prefix[:-1])
    results = sorted(results, key=topic_score, reverse=True)
    return results

def topic_score(topic):
    return r.zscore(topic_hot_key, topic)

def main():
    try:
        results = db['topics'].find(sort=[('ts', 1)])
    except Exception, e:
        print e
    for result in results:
       topic = result['topic']
       count = result['count']
       r.zadd(topic_hot_key, topic, count)
       for index, word in enumerate(topic):
           prefix = topic[:index]
           r.zadd(topic_suggest_key, prefix, 0)
       r.zadd(topic_suggest_key, topic+'*', 0)

def test():
    q = raw_input('Enter word for topic suggest:')
    q = q.decode('utf-8')
    results = suggest(q)
    for result in results:
        print result

if __name__ == '__main__': main()
        
