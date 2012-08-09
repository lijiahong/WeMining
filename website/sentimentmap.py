#-*- coding:utf-8 -*-

'''微博话题分析页面以及相关数据接口
'''

import json
import urllib
import time
import web
import random
import math

from tokenizer.fenci import cut
from config import getUser, getDB
from weibo_search import WeiboSearch
from weibo import _obj_hook

import sys
sys.path.append('..')

from mining.emotion import EmotionClassifier

render = web.template.render('./templates/', base='layout')

urls = ('/sentimentmap/', )

class handler():
    def GET(self):
        pass

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


def analysis_data(keywords, limit=10000):
    db = getDB()
    dt = {}
    dt_province = {}
    search = WeiboSearch()
    texts, results = search.query(job='emotion', keywords=keywords, limit=limit)
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
        results.append({'ts': ts,
                       'province_level': dic['province'],
                       'most_province': dic['most'],
                       'detail_province': dic['detail']
                })
    return results

