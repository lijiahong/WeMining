#-*- coding:utf-8 -*-

import json
import web

from config import getDB, cut

urls = ('/api/search/search.json', )

class handler():
    def GET(self):
        form = web.input(q=None,t=None)
        search = Search()
        keywords = cut(form.q)
        return json.dumps(search.query(keywords, all=True if form.t else False))


class Search(object):
    def __init__(self):
        self.db = getDB()
    
    def query(self, keywords, all=True, **kw):
        query_dict = {}
        query_dict.update(kw)
        if all:
            query_dict['_keywords'] =  {'$all': keywords}
        else:
            query_dict['_keywords'] =  {'$in': keywords}
        return self.db['public_statuses'].find(query_dict, sort=[('ts', pymongo.ASCENDING)])    

                 
def main():
    search = Search()
    for r in search.query([u'北京', u'雷雨'], location=u'北京'):
        print r['ts']

if __name__ == '__main__': main()

