#-*- coding:utf-8 -*-

import json
import xapian
import urllib
import time

from config import getDB
from weibo import _obj_hook

import sys
sys.path.append('..')

from mining.emotion import EmotionClassifier

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

    def repost_chain_query(self, begin=None, end=None, keywords=[], limit=1000):
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

    def emotion_query(self, begin=None, end=None, keywords=[], limit=1000):
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
        texts = []
        for m in matches:
            result = {}
            result['ts'] = xapian.sortable_unserialise(m.document.get_value(self.timestampvi))
            result['location'] = m.document.get_value(self.loctvi)
            texts.append(json.loads(m.document.get_value(self.keywordsvi)))
            results.append(result)
        return texts, results

    def spread_query(self, begin=None, end=None, keywords=[], limit=1000):
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
            results['id'] = m.document.get_value(self.widvi)
            result['location'] = m.document.get_value(self.loctvi)
            result['repost_location'] = m.document.get_value(self.reploctvi)
            result['timestamp'] = xapian.sortable_unserialise(m.document.get_value(self.timestampvi))
            results.append(result)
        return results

    def query(self, job=None, **kw):
        if job:
            func = getattr(self, job+'_query')
            return func(**kw)

def getLatLon(db, location):
    try:
        tokens = location.split(' ')
        if len(tokens) == 1:
            province, district = tokens[0], None
        elif len(tokens) == 2:
            province, district = tokens[0], tokens[1]
        if province == u'其他':
            return 'null'
    except Exception, e:
        print e
        return 'null'
    if not db.location.find({'location': location}).count():
        if province == u'海外':
            if not district or district == u'其他':
                return 'null'
            q = location.encode('utf-8')
        else:
            q = (u'中国'+location).encode('utf-8')
        url = 'http://ditu.google.cn/maps/api/geocode/json?address='+urllib.quote(q)+'&sensor=false'
        try:
            result = urllib.urlopen(url).read()
            jsons = json.loads(result, object_hook=_obj_hook)
            #print jsons
            if jsons.status == 'OK':
                p = jsons.results[0].geometry.location
                latlon = '%s %s' % (p.lat, p.lng)
                print latlon
            else:
                return 'null'
        except Exception, e:
            print '%s: Fetch google map api url error: %s!' % (time.ctime(), e)
            return None
        db.location.save({'location': location, 'latlon': latlon})
        time.sleep(1)
    else:
        latlon = db.location.find_one({'location': location})['latlon']
    return latlon

     
def main():
    db = getDB()
    dt = {}
    dt_province = {}
    search = WeiboSearch()
    texts, results = search.query(job='emotion', keywords=[u'薄熙来'], limit=10000)
    ec = EmotionClassifier()
    emotions = ec.predict(texts)
    for result, emotion in zip(results, emotions):
        ts = result['ts']
        location = result['location'].decode('utf-8')
        province = location.split(' ')[0]
        assert province
        if province == u'其他' or province == u'海外':
            continue
        if ts not in dt:
            dt[ts] = {}
            dt[ts]['detail'] = []
            dt_province[ts] = {}
        if location not in dt[ts]:
            dt[ts][location] = [0, 0, 0]
        if province not in dt_province[ts]:
            dt_province[ts][province] = [0, 0, 0]
        dt[ts][location][emotion-1] += 1
        dt_province[ts][province][emotion-1] += 1
    for ts in dt:
        for location in dt[ts]:
            latlon = getLatLon(db, location)
            emotion = dt[ts][location][:]
            dt[ts]['detail'].append([latlon, emotion])
    max_emotions = [0, 0, 0]
    min_emotions =[-1, -1, -1]
    for ts in dt_province:
        most = [0, 0, 0]
        most_province = ['', '', '']
        for location in dt_province[ts]:
            arr = dt_province[ts][location]
            for i in range(len(arr)):
                if max_emotions[i] < arr[i]:
                    max_emotions[i] = arr[i]
                if min_emotions[i] > arr[i]:
                    min_emotions[i] = arr[i]
                if most[i] < arr[i]:
                    most_province[i] = location
                    most[i] = arr[i]
        dt[ts]['most'] = []
        for p in most_province:
            if p:
                dt[ts]['most'].append([p, dt_province[ts][p]])
            else:
                dt[ts]['most'].append([p, None])
    for ts in dt_province:
        province = {}      
        for location in dt_province[ts]:
            emotions = dt_province[ts][location]
            current_max = max(emotions)
            emotion_type = emotions.index(current_max)
            max_emotion = max_emotions[emotion_type]
            min_emotion = min_emotions[emotion_type]
            j = 0
            for i in range(min_emotion, max_emotion+1):
                if current_max > i:
                    j += 1
                else:
                    break
            level = j*1.0/(max_emotion-min_emotion)
            assert level > 0
            if 0 <= level <= 0.2:
                level = 0
            elif 0.2 <= level <= 0.4:
                level = 1
            elif 0.4 <= level <= 0.6:
                level = 2
            elif 0.6 <= level <= 0.8:
                level = 3
            else:
                level = 4
            province[location] = [emotion_type, level]
        dt[ts]['province'] = province
    
    dt = sorted(dt.iteritems(), key=lambda(x, y): x)
    results = []
    for ts, dic in dt:
        print ts
        print dic['province']
        print dic['most']
        print dic['detail']
        results.append({'ts': ts,
                       'province_level': dic['province'],
                       'most_province': dic['most'],
                       'detail_province': dic['detail']
                })
    f = open('test.js', 'w')
    f.write(json.dumps(results))
    f.close()
    

if __name__ == '__main__': main()

