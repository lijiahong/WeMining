#-*- coding:utf-8 -*-

import re

import sys
sys.path.append('..')

import re
from config import getDB

class WeiboSearch(object):
    def __init__(self):
        self.db = getDB()

    def query(self, job=None, **kw):
        if job:
            func = getattr(self, job+'_query')
            return func(**kw)
    
    def repost_chain_query(self, begin=None, end=None, keywords=[], limit=2000):
        if not len(keywords) > 0:
            return None
        ts_query = None
        if begin and end:
            ts_query = {'$gte': begin, '$lte': end}
        elif begin:
            ts_query = {'$gte': begin}
        elif end:
            ts_query = {'$lte': end}
        if not ts_query:
            matches = self.db['user_statuses'].find({'_keywords': {'$all': keywords}}, sort=[('ts',  1)]).limit(limit)
        else:
            matches = self.db['user_statuses'].find({'_keywords': {'$all': keywords}, 'ts': ts_query}, sort=[('ts',  1)]).limit(limit)
        results = []
        for m in matches:
            result = {}
            result['username'] = m['name'].encode('utf-8')
            repnames_arr = []
            text = m['text']
            if re.search(u'&', text):
                continue
            for username in re.findall(r'//@(\S+?):', text):
                if username not in repnames_arr:
                    repnames_arr.append(username)
            try:
                repostname = weibo['repost']['username']
                repnames_arr.append(repostname)
            except:
                pass
            result['repost_chain'] = repnames_arr
            result['timestamp'] = m['ts']
            result['text'] = m['text']
            result['keywords'] = m['_keywords']
            results.append(result)
        return results
    
    def emotion_query(self, begin=None, end=None, keywords=[], limit=10000):
        if not len(keywords) > 0:
            return None
        ts_query = None
        if begin and end:
            ts_query = {'$gte': begin, 'lte': end}
        elif begin:
            ts_query = {'$gte': begin}
        elif end:
            ts_query = {'lte': end}
        if not ts_query:
            matches = self.db['user_statuses'].find({'_keywords': {'$all': keywords}}, sort=[('ts',  1)]).limit(limit)
        else:
            matches = self.db['user_statuses'].find({'_keywords': {'$all': keywords}, 'ts': ts_query}, sort=[('ts',  1)]).limit(limit)
        results = []
        texts = []
        for m in matches:
            result = {}
            result['location'] = m['location'].encode('utf-8')
            result['ts'] = m['ts']
            result['_id'] = m['_id']
            texts.append(m['_keywords'])
            results.append(result)
        return texts, results 

    def spread_query(self, begin=None, end=None, keywords=[], limit=10000):
        if not len(keywords) > 0:
            return None
        ts_query = None
        if begin and end:
            ts_query = {'$gte': begin, '$lte': end}
        elif begin:
            ts_query = {'$gte': begin}
        elif end:
            ts_query = {'$lte': end}
        if not ts_query:
            matches = self.db['user_statuses'].find({'_keywords': {'$all': keywords}}, sort=[('ts',  1)]).limit(limit)
        else:
            matches = self.db['user_statuses'].find({'_keywords': {'$all': keywords}, 'ts': ts_query}, sort=[('ts',  1)]).limit(limit)
        results = []
        for m in matches:
            result = {}
            result['location'] = m['location'].encode('utf-8')
            try:
                result['repost_location'] = m['repost']['location'].encode('utf-8')
            except KeyError:
                result['repost_location'] = None
            result['timestamp'] = m['ts']
            result['_id'] = m['_id']
            results.append(result)
        return results

    def count(self, begin=None, end=None, keywords=[], limit=100000):
        if not len(keywords) > 0:
            return None
        ts_query = None
        if begin and end:
            ts_query = {'$gte': begin, '$lte': end}
        elif begin:
            ts_query = {'$gte': begin}
        elif end:
            ts_query = {'$lte': end}
        if not ts_query:
            results = self.db['user_statuses'].find({'_keywords': {'$all': keywords}}).limit(limit)
        else:
            results = self.db['user_statuses'].find({'_keywords': {'$all': keywords}, 'ts': ts_query}).limit(limit)
        return results.count()

def main():
    search = WeiboSearch()
    print search.count(keywords=[u'钓鱼岛'])
    results = search.query(job='repost_chain', keywords=[u'钓鱼岛'], begin=1284480000, end=1347984000)
    for r in results:
        print r['timestamp']

if __name__ == '__main__': main()
