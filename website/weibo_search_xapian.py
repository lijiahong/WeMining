#-*- coding:utf-8 -*-

import json
import xapian
import time

import sys
sys.path.append('..')

from mining.emotion import EmotionClassifier

class WeiboSearch(object):
    def __init__(self, dbpath='./new_userstatuses/'):
        database = xapian.Database(dbpath)
        enquire = xapian.Enquire(database)
        qp = xapian.QueryParser()
        stemmer = xapian.Stem('english')
        qp.set_stemmer(stemmer)
        qp.set_database(database)
        qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        self.qp = qp
        self.enquire = enquire
        self.emotionvi = 0
        self.keywordsvi = 1
        self.timestampvi = 2
        self.loctvi = 3
        self.reploctvi = 4
        self.emotiononlyvi = 5
        self.usernamevi = 6
        self.hashtagsvi = 7
        self.uidvi = 8
        self.repnameslistvi = 9
        self.widvi = 10

    def repost_chain_query(self, begin=None, end=None, keywords=[], limit=50000):
        if not len(keywords) > 0:
            return None

        self.qp.add_valuerangeprocessor(xapian.NumberValueRangeProcessor(self.timestampvi, ''))

        keywords = [keyword.lower() for keyword in keywords]
        wordsquery = xapian.Query(xapian.Query.OP_AND,keywords)

        if begin and end:
            timequerystr = str(begin) + '..' + str(end)
            timequery = self.qp.parse_query(timequerystr)
            query = xapian.Query(xapian.Query.OP_AND,[timequery, wordsquery])
        else:
            query = wordsquery
        self.enquire.set_query(query)
        self.enquire.set_sort_by_value(self.timestampvi, False)
        matches = self.enquire.get_mset(0, limit)
        results = []
        for m in matches:
            result = {}
            result['username'] = m.document.get_value(self.usernamevi)
            result['repost_chain'] = json.loads(m.document.get_value(self.repnameslistvi))
            result['timestamp'] = xapian.sortable_unserialise(m.document.get_value(self.timestampvi))
            result['keywords'] = json.loads(m.document.get_value(self.keywordsvi))
            results.append(result)
        return results

    def emotion_query(self, begin=None, end=None, keywords=[], limit=50000):
        if not len(keywords) > 0:
            return None

        self.qp.add_valuerangeprocessor(xapian.NumberValueRangeProcessor(self.timestampvi, ''))

        keywords = [keyword.lower() for keyword in keywords]
        wordsquery = xapian.Query(xapian.Query.OP_AND,keywords)

        if begin and end:
            timequerystr = str(begin) + '..' + str(end)
            timequery = self.qp.parse_query(timequerystr)
            query = xapian.Query(xapian.Query.OP_AND,[timequery, wordsquery])
        else:
            query = wordsquery
        self.enquire.set_query(query)
        self.enquire.set_sort_by_value(self.timestampvi, False)
        matches = self.enquire.get_mset(0, limit)
        results = []
        texts = []
        for m in matches:
            result = {}
            result['ts'] = xapian.sortable_unserialise(m.document.get_value(self.timestampvi))
            result['location'] = m.document.get_value(self.loctvi)
            texts.append(json.loads(m.document.get_value(self.keywordsvi)))
            results.append(result)
        return texts, results

    def spread_query(self, begin=None, end=None, keywords=[], limit=50000):
        if not len(keywords) > 0:
            return None

        self.qp.add_valuerangeprocessor(xapian.NumberValueRangeProcessor(self.timestampvi, ''))

        keywords = [keyword.lower() for keyword in keywords]
        wordsquery = xapian.Query(xapian.Query.OP_AND,keywords)

        if begin and end:
            timequerystr = str(begin) + '..' + str(end)
            timequery = self.qp.parse_query(timequerystr)
            query = xapian.Query(xapian.Query.OP_AND,[timequery, wordsquery])
        else:
            query = wordsquery
        self.enquire.set_query(query)
        self.enquire.set_sort_by_value(self.timestampvi, False)
        matches = self.enquire.get_mset(0, limit)
        results = []
        for m in matches:
            result = {}
            result['location'] = m.document.get_value(self.loctvi)
            result['repost_location'] = m.document.get_value(self.reploctvi)
            result['timestamp'] = xapian.sortable_unserialise(m.document.get_value(self.timestampvi))
            result['_id'] = m.document.get_value(self.widvi)
            results.append(result)
        return results

    def count(self, begin=None, end=None, keywords=[], limit=100000):
        if not len(keywords) > 0:
            return None

        self.qp.add_valuerangeprocessor(xapian.NumberValueRangeProcessor(self.timestampvi, ''))

        keywords = [keyword.lower() for keyword in keywords]
        wordsquery = xapian.Query(xapian.Query.OP_AND,keywords)

        if begin and end:
            timequerystr = str(begin) + '..'+ str(end)
            timequery = self.qp.parse_query(timequerystr)
            query = xapian.Query(xapian.Query.OP_AND,[timequery, wordsquery])
        else:
            query = wordsquery
        self.enquire.set_query(query)
        self.enquire.set_sort_by_value(self.timestampvi, False)
        matches = self.enquire.get_mset(0, limit)
        return matches.size()

    def query(self, job=None, **kw):
        if job:
            func = getattr(self, job+'_query')
            return func(**kw)

def main():
    search = WeiboSearch()
    print search.count(keywords=[u'薄熙来'])
    

if __name__ == '__main__': main()

