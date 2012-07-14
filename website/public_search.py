#-*- coding:utf-8 -*-

import json
import web
import pymongo

import sys
sys.path.append('..')

from config import getDB
from tokenizer.fenci import cut

urls = ('/api/public/search.json', )

class handler():
    def GET(self):
        form = web.input(q=None,t=None, page=None)
        search = Search()
        keywords = cut(form.q, f=['n', 'nr', 'ns', 'nt'])
        if not form.page:
            form.page = 1
        return json.dumps(search.query(keywords, all=True if not form.t else False, page=int(form.page)))


class Search(object):
    def __init__(self):
        self.db = getDB()
    
    def query(self, keywords, all=True, page=1, **kw):
        query_dict = {}
        query_dict.update(kw)
        if all:
            query_dict['_keywords'] =  {'$all': keywords}
        else:
            query_dict['_keywords'] =  {'$in': keywords}
        try:
            results = self.db['public_statuses'].find(query_dict, sort=[('ts', pymongo.ASCENDING)]).skip((page-1)*20).limit(20)
        except:
            return {'error': 'something wrong'}
        return list(results)

                 
def main():
    search = Search()
    for r in search.query([u'北京', u'雷雨'], location=u'北京'):
        print r['ts']

if __name__ == '__main__': main()

