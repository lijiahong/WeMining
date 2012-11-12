#!/usr/bin/env python
#-*-coding:utf-8-*-


import time
import json
import operator
import codecs

import xapian

def unix2local(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

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

    def topic_query(self, begin=None, end=None, limit=100000):
        self.qp.add_valuerangeprocessor(xapian.NumberValueRangeProcessor(self.timestampvi, ''))
        if begin and end:
            timequerystr = str(date2ts(begin)) + '..' + str(date2ts(end))
            timequery = self.qp.parse_query(timequerystr)
        else:
            return None
        self.enquire.set_query(timequery)
        self.enquire.set_sort_by_value(self.timestampvi, False)
        matches = self.enquire.get_mset(0, limit)
        ts_arr = []
        results = []
        total_keywords_count = {}
        for match in matches:
            result = {}
            result['ts'] = xapian.sortable_unserialise(match.document.get_value(self.timestampvi))
            result['keywords'] = list(set(json.loads(match.document.get_value(self.keywordsvi))))
            for k in result['keywords']:
                if k not in total_keywords_count:
                    total_keywords_count[k] = 0
                total_keywords_count[k] += 1
            ts_arr.append(result['ts'])
            results.append(result)
        return ts_arr, results, total_keywords_count

def partition(ts_arr, data, window_size=24*60*60):
    ts_series = []
    ts_start = ts_arr[0]
    ts_end = ts_arr[-1]
    each_step = window_size
    ts_current = ts_start
    data_cursor = -1
    groups_keywords_count = []
    while ts_current <= ts_end:
        s_ts = ts_current
        f_ts = ts_current + each_step
        ts_series.append([s_ts, f_ts])
        groups_size = []
        group = []
        for d in data[data_cursor+1:]:
            ts = d['ts']
            group.append(d)
            if ts >= f_ts:
                break
            data_cursor += 1
        groups_size.append(len(group))
        if len(group):
            group_keywords_count = {}
            for d in group:
                for k in d['keywords']:
                    if k not in group_keywords_count:
                        group_keywords_count[k] = 0
                    group_keywords_count[k] += 1
            groups_keywords_count.append(group_keywords_count)
        ts_current += each_step
    return ts_series, groups_keywords_count, groups_size

def burst(ts_series, groups_keywords_count, total_keywords_count, groups_size, total_size):
    word_burst_in_groups = []
    for period, group_keywords_count, group_size in zip(ts_series, groups_keywords_count, groups_size):
        word_burst_in_group = {}
        for keyword in group_keywords_count.keys():
            A = group_keywords_count[keyword]
            B = total_keywords_count[keyword] - A
            C = group_size - A
            D = total_size - total_keywords_count[keyword] - C
            try:
                word_burst_in_group[keyword] = (A + B + C + D) * ((A*D - B*C) ** 2) * 1.0 / ((A + B) * (C + D) * (A + C) * (B + D))
            except ZeroDivisionError:
                word_burst_in_group[keyword] = 0
        word_burst_in_groups.append(word_burst_in_group)
    keywords_burst = {}
    for keyword in total_keywords_count.keys():
        for group in word_burst_in_groups:
            if keyword in group:
                if keyword not in keywords_burst:
                    keywords_burst[keyword] = 0
                keywords_burst[keyword] += group[keyword]
    keywords_brust_list = sorted(keywords_burst.iteritems(), key=operator.itemgetter(1), reverse=True)
    f = codecs.open('results.txt', 'w', encoding='utf-8')
    for key, value in keywords_brust_list[:100]:
        f.write('%s %s\n' % (key, value))
    f.close()
            

def main():
    time_start = '2012-9-1'
    time_end = '2012-10-1'
    search = Search()
    ts_arr, results, total_keywords_count = search.topic_query(begin=time_start, end=time_end)
    total_size = len(results)
    print 'find %s statuses from %s to %s.' % (total_size, time_start, time_end)
    ts_series, groups_keywords_count, groups_size = partition(ts_arr, results, window_size=24*60*60)
    print 'partition ok.'
    burst(ts_series, groups_keywords_count, total_keywords_count, groups_size, total_size)

if __name__ == '__main__': main()
