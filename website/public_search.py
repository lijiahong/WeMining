#-*- coding:utf-8 -*-

import json
import web
import pymongo

from config import getDB, cut

urls = ('/api/public/search.json', )

class handler():
    def GET(self):
        form = web.input(q=None,t=None, start=None, end=None, page=None)
        search = Search()
        keywords = cut(form.q)
        args = {}
        if form.start:
            args['ts'] = {'$gte': form.start}
        if form.end:
            args['ts'] = {'$lte': form.end}
        if not form.page:
            form.page = 1
        return json.dumps(search.query(keywords, all=True if not form.t else False, page=form.page, **args))


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
        results = self.db['public_statuses'].find(query_dict, sort=[('ts', pymongo.ASCENDING)]).skip((page-1)*20).limit(20)
        return list(results)

                 
def main():
    search = Search()
    for r in search.query([u'北京', u'雷雨'], location=u'北京'):
        print r['ts']

if __name__ == '__main__': main()

