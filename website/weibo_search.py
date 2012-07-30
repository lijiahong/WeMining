#-*- coding:utf-8 -*-

import json
import xapian

class WeiboSearch(object):
    def __init__(self, dbpath='/home/mirage/Downloads/weiboxa/han'):
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

    def query(self, begin=None, end=None, keywords=[], limit=1000):
        if not len(keywords) > 0:
            return None

        self.qp.add_valuerangeprocessor(xapian.NumberValueRangeProcessor(self.timestampvi, ''))

        keywords = [keyword.lower() for keyword in keywords]
        wordsquery = xapian.Query(xapian.Query.OP_AND,keywords)

        if begin and end:
            timequerystr = begin+'..'+end
            timequery = self.qp.parse_query(timequerystr)
            query = xapian.Query(xapian.Query.OP_AND,[timequery, wordsquery])
        else:
            query = wordsquery
        self.enquire.set_query(query)
        self.enquire.set_sort_by_value(self.timestampvi,False)
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

        
def main():
    search = WeiboSearch()
    for result in search.query(keywords=[u'薄熙来'], limit=10000):
        r = result['repost_chain']
        if len(r) > 2:
            print result['username']
            for name in r:
                print name.encode('utf-8')
            print '------'

if __name__ == '__main__': main()

