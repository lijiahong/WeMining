#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import json
import codecs
import datetime

from config import getDB

import sys
sys.path.append('..')

from mining.emotion import EmotionClassifier

def ts2date(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

def date2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

def main():
    args = sys.argv
    if len(args) > 2:
        start_day = args[0]
        end_day = args[1]
    else:
        start_day = '2012-7-1'
        end_day = ts2date(time.time())

    db = getDB()
    start_ts = date2ts(start_day)
    end_ts = date2ts(end_day)
    results = db['public_statuses'].find({'ts': {'$gte': start_ts, '$lte': end_ts}})
    dt = {}
    dt_tmline_arr = []
    ec = EmotionClassifier()
    for status in results:
        ts = status['ts']
        date = ts2date(ts)
        if not date in dt:
            dt[date] = {'texts': []}
        dt[date]['texts'].append(status['_keywords'])
    for date in dt:
        count = {1: 0, 2: 0, 3: 0}
        total = 0.0
        emotions = ec.predict(dt[date]['texts'])
        for emotion in emotions:
            if emotion:
                count[emotion] += 1
                total += 1
        dt_tmline_arr.append([date2ts(date), count[1]/total, count[2]/total, count[3]/total])
    dt_tmline_arr = sorted(dt_tmline_arr, key=lambda x: x[0])
    f = codecs.open('./html/static/js/emotion_summary.js', 'w', encoding='utf-8')
    f.write('var emotion_tmline_arr = [')
    for d in dt_tmline_arr[:-1]:
        f.write("[new Date(%s), %s, %s, %s]," % (ts2date(d[0]), d[1], d[2], d[3]))
    d = dt_tmline_arr[-1]
    f.write("[new Date(%s), %s, %s, %s]" % (ts2date(d[0]), d[1], d[2], d[3]))
    f.write(']')
    f.close()

if __name__ == '__main__': main()
