#-*- coding:utf-8 -*-

import pymongo
from config import db


class Search(object):
    
    def __init__(self):
        pass
    
    def query(self, keywords, all=True, **kw):
        query_dict = {}
        query_dict.update(kw)
        if all:
            query_dict['_keywords'] =  {'$all': keywords}
        else:
            query_dict['_keywords'] =  {'$in': keywords}
        return db['public_statuses'].find(query_dict, sort=[('ts', pymongo.ASCENDING)])    

                 
def main():
    search = Search()
    for r in search.query([u'北京', u'雷雨'], location=u'北京'):
        print r['ts']

if __name__ == '__main__': main()

