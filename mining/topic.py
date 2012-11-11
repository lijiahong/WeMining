#!/usr/bin/env python
#-*-coding:utf-8-*-


import time
import xapian
import codecs

def date2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

class Search(object):
    def __init__(self, dbpath='/opt/data/index/userstatuses/'):
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

    def topic_query(self, begin=None, end=None, limit=5000000):
        self.qp.add_valuerangeprocessor(xapian.NumberValueRangeProcessor(self.timestampvi, ''))
        if begin and end:
            timequerystr = str(begin) + '..' + str(end)
            timequery = self.qp.parse_query(timequerystr)
        else:
            return None
        self.enquire.set_query(timequery)
        self.enquire.set_sort_by_value(self.timestampvi, False)
        matches = self.enquire.get_mset(0, limit)
        print matches.size()

def main():
    time_start = date2ts('2012-9-1')
    time_end = date2ts('2012-10-1')
    search = Search()
    search.topic_query(begin=time_start, end=time_end)

if __name__ == '__main__': main()
