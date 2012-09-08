#-*- coding:utf-8 -*-

'''微博话题分析页面以及相关数据接口
'''

import json
import urllib
import time
import web
import random
import math

import sys
sys.path.append('..')

from tokenizer.fenci import cut
from config import getUser, getDB
from weibo_search import WeiboSearch
from weibo import _obj_hook

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


def analysis_data(keywords, limit=10000, section=25):
    '''[
	{
		ts:122838328,
		province:{
			"北京":[emotion_type,level],
			"上海":[emotion_type,level],
			...
		},
		most_province:[
		        //最悲伤
			[
				"北京",
				//悲伤、愤怒、高兴 数量
				[30, 20, 10]
			],

			//最愤怒
			["上海", [20, 30, 10]],

                        //最高兴
			["上海", [20, 10, 30]]
		],
		detail:[
			[
				//经纬度
				'22.1638446 113.5549937',
                                //悲伤、愤怒、高兴 数量
				[12, 11, 10]
			],

                        ['20.1638446 110.5549937', [13, 12, 11]],

			...

		]
	},

	{
	   ...
	},
	
	...
       ]
    '''
    db = getDB()
    dt = {}
    dt_province = {}
    search = WeiboSearch()
    texts, results = search.query(job='emotion', keywords=keywords, limit=limit)
    ec = EmotionClassifier()
    emotions = ec.predict(texts)
    ts_dic = {}
    ts_final = {}
    ts_arr = []
    for result, emotion in zip(results, emotions):
        ts = result['ts']
        ts_arr.append(ts)
        location = result['location'].decode('utf-8')
        if ts not in ts_dic:
            ts_dic[ts] = {}
        if location not in ts_dic[ts]:
            ts_dic[ts][location] = [0, 0, 0]
        ts_dic[ts][location][emotion-1] += 1
    ts_arr = sorted(list(set(ts_arr)))
    ts_series = []
    each_step = int(math.floor(len(ts_arr)/section))
    index = 0
    index += each_step;
    while index < len(ts_arr):
        p_index = index - each_step
        s_ts = ts_arr[p_index]
        f_ts = ts_arr[index]
        ts_final[s_ts] = {}
        for t in ts_arr[p_index:index+1]:
            data = ts_dic[t]
            for location in data:
                if location not in ts_final[s_ts]:
                    ts_final[s_ts][location] = [0, 0, 0]
                for i in range(len(data[location])):
                    ts_final[s_ts][location][i] += data[location][i]
        index += each_step;
    if index != len(ts_arr)-1:
        s_ts = f_ts
        f_ts = ts_arr[-1]
        ts_final[s_ts] = {}
        for t in ts_arr[p_index:index+1]:
            data = ts_dic[t]
            for location in data:
                if location not in ts_final[s_ts]:
                    ts_final[s_ts][location] = [0, 0, 0]
                for i in range(len(data[location])):
                    ts_final[s_ts][location][i] += data[location][i]
    for ts in ts_final:
        for location in ts_final[ts]:
            province = location.split(' ')[0]
            assert province
            data = ts_final[ts][location]
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
            for i in range(len(data)):
                dt[ts][location][i] += data[i]
                dt_province[ts][province][i] += data[i]
    for ts in dt:
        for location in dt[ts]:
            if location == 'detail':
                continue
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

def main():
    count = 0
    for res in analysis_data([u'薄熙来'], limit=100):
        count += 1
        print res['ts']
    print count

if __name__ == '__main__': main()
