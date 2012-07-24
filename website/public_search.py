#-*- coding:utf-8 -*-

import json
import web
import pymongo
import math

import sys
sys.path.append('..')

from mining.emotion import EmotionClassifier
from config import getDB
from tokenizer.fenci import cut

urls = ('/api/public/search.json', )

class handler():
    def GET(self):
        form = web.input(q=None,t=None, e=None, page=None)
        search = Search()
        if not form.q:
            return json.dumps({'error': 'need keywords for search'})
        keywords = cut(form.q, f=['n', 'nr', 'ns', 'nt'])
        if not form.page:
            form.page = 1
        return json.dumps(search.query(keywords, all=True if not form.t else False, emotion=True if form.e else False, page=int(form.page)))


class Search(object):
    def __init__(self):
        self.db = getDB()
    
    def query(self, keywords, all=True, emotion=False, page=1, limit=200, **kw):
        query_dict = {}
        query_dict.update(kw)
        if all:
            query_dict['_keywords'] =  {'$all': keywords}
        else:
            query_dict['_keywords'] =  {'$in': keywords}
        try:
            results = self.db['public_statuses'].find(query_dict, sort=[('ts',  pymongo.DESCENDING)])
            pages = int(math.ceil(results.count()/200.0))
            results = results.skip((page-1)*200).limit(limit)
            texts = []
            statuses = []
            for status in results:
                texts.append(status['_keywords'])
                statuses.append(status)
            if emotion:
                ec = EmotionClassifier()
                emotions = ec.predict(texts)
                return {'results': statuses, 'page': page, 'total_pages': pages, 'emotions': emotions}
            return {'results': statuses, 'page': page, 'total_pages': pages}
        except:
            return {'error': 'something wrong'}

                 
def main():
    search = Search()
    for r in search.query([u'北京', u'雷雨'], location=u'北京'):
        print r['ts']

if __name__ == '__main__': main()

