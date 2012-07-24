#-*- coding:utf-8 -*-

'''微博话题分析页面以及相关数据接口
'''

import json
import time
import datetime
import web
import operator
import random
import math

from datetime import date
from tokenizer.fenci import cut
from public_search import Search

search = Search()

render = web.template.render('./templates/')

urls = ('/topicweibo/analysis', )

class handler():
    def GET(self):
        form = web.input(topic=None, json=None)
        topic = form.topic
        json = form.json
        if topic and json:
            return analysis_data(topic)
        elif topic:
            return render.topicanalysis()
        else:
            return render.topicweibo()

def analysis_data(topic):
    keywords = cut(topic, f=['n', 'nr', 'ns', 'nt'])
    results = search.query(keywords, emotion=True, limit=1000)
    statuses = results['results']
    emotions = results['emotions']
    timedist_week = time_dist(statuses, timemodule='week')
    timedist_day = time_dist(statuses, timemodule='day')
    random_statuses = random_statuses_f(statuses)
    mood_timeline = mood_timeline_f(statuses, emotions)
    mood_location = mood_location_f(statuses, emotions)
    china_map_count = map_count(statuses)
    return json.dumps({'timedist_week': timedist_week,
                       'timedist_day': timedist_day,
                       'random_statuses': random_statuses,
                       'mood_timeline': mood_timeline,
                       'mood_location': mood_location,
                       'china_map_count': china_map_count,
            })

def map_count(statuses):
    raw = []
    for s in statuses:
        loc = s['location']
        if getProvince(loc) != -1:
            raw.append(getProvince(loc))
    rawhash = {}
    for r in raw:
        if not rawhash.has_key(r):
             rawhash[r]=[1]
        else:
             rawhash[r].append(1)
    result = {}
    for k in rawhash.keys():
        result[k]=len(rawhash[k])
    return province_color_map(result)

def province_color_map(city_count):
    total_count = sum(city_count.values())
    city_sorted = sorted(city_count.iteritems(), key=lambda(k, v): v, reverse=True)
    city_color = {}
    city_count = {}
    city_summary = []
    color = ['#000079', '#0f1486', '#1e2893', '#2d3ca1', '#3c51ae', '#4b65bc', '#5a79c9', '#698ed6', '#78a2e4', '#87b6f1', '#96cafe']
    if len(city_sorted) > len(color):
        n = int(math.ceil(len(city_sorted)*1.0/len(color)))
        for i in range(0, len(city_sorted), n):
            for j in range(n):
                if i+j < len(city_sorted):
                    city, count = city_sorted[i+j]
                    if count == 0:
                        continue
                    city_color[city] = color[i/n]
                    rank = i+j+1
                    percent = str(int(count*1000/total_count)/10.0)+'%'
                    if rank <= 10:
                        city_summary.append([rank, city, percent])
                    city_count[city] = [count, rank, percent]
    else:
        for index, x in enumerate(city_sorted):
            if count:
                city, count = x
                city_color[city] =  "%s" % color[index]
                percent = str(int(count*1000/total_count)/10.0)+'%'
                rank = index+1
                if rank <= 10:
                    city_summary.append([rank, city, percent])
                city_count[city] = [count, rank, percent]
    data = {'count': city_count,
            'color': city_color,
            'summary': city_summary}
    return data

def ts2date(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

def date2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

def location_count(statuses, emotions):
    count = {}
    most = [0, 0, 0]
    most_city = ['', '', '']
    for status, emotion in zip(statuses, emotions):
        if emotion:
            location = status['location'].split(' ')[0]
            if location == u'其他' or location == u'海外':
                continue
            if location in count:
                count[location][emotion-1] += 1
            else:
                count[location] = [0, 0, 0]
                count[location][emotion-1] = 1
    for city in count:
        arr = count[city]
        total = 0
        total = sum(arr)
        for i in range(len(arr)):
            arr[i] /= total
            if most[i] < arr[i]:
                most_city[i] = city
                most[i] = arr[i]
    return {'count': count, 'most': most_city}

def mood_location_f(statuses, emotions):
    dt = {}
    location_emotion_tmline = []
    for status, emotion in zip(statuses, emotions):
        date = ts2date(status['ts'])
        if date not in dt:
            dt[date] = {'statuses': [], 'emotions': []}
        dt[date]['statuses'].append(status)
        dt[date]['emotions'].append(emotion)
    dt = sorted(dt.iteritems(), key=lambda(k, v): date2ts(k), reverse=True)
    for date, d in dt:
        data = location_count(d['statuses'], d['emotions'])
        count = data['count']
        most = data['most']
        location_emotion_tmline.append([date, count, most])
    return location_emotion_tmline

def mood_timeline_f(statuses, emotions):
    result, emotions = statuses, emotions
    raw = []
    for i in range(0,len(result)):
        if result[i]["location"].split(" ")[0] == u"海外" or result[i]["location"].split(" ")[0] == u"其他":
            continue
        else:
            raw.append([date.fromtimestamp(result[i]["ts"]),result[i]["location"].split(" ")[0],emotions[i]])
    ts_em = {}
    for r in raw:
        if not ts_em.has_key(r[0]):
            ts_em[r[0]] = [r[2]]
        else:
            ts_em[r[0]].append(r[2])
    ts_em_list = []
    for k in ts_em:
        sad = 0
        angry = 0
        happy = 0
        for e in ts_em[k]:
            
            if e == 1:
                sad = sad + 1
            if e == 2:
                angry = angry + 1
            if e == 3:
                happy = happy + 1
        total = sad + angry + happy
        if total == 0:
            continue
        ts_em_list.append([str(k),sad/total,angry/total,happy/total])
    return ts_em_list

def random_statuses_f(statuses, count=5):
    results = []
    random.shuffle(statuses)
    for status in statuses[:count]:
         hashtags =  status["hashtags"]
         hashtags_str = ""
         if hashtags:
             for h in hashtags:
                 hashtags_str = hashtags_str + h + ","
         results.append([status["uid"], status["_id"], str(date.fromtimestamp(status["ts"])), status["location"], status["name"], status["text"], hashtags_str]) 
    return results

def time_dist(statuses, timemodule="all", daypoint=None):
    if timemodule == "all":
        time2id = {}
        for s in statuses:
            if not time2id.has_key(int(s['ts'])):
                time2id[int(s['ts'])] =  [s['_id']]
            else:
                time2id[int(s['ts'])].append(s['_id'])
        raw = sorted(time2id.iteritems(),key=lambda(k,v):k)
        result = []
        for r in raw:
            result.append([r[0]*1000,len(r[1])])
        return result
    if timemodule == "week":
        day2id = {}
        for s in statuses:
            ts = s['ts']
            weiboid = s['_id']
            da = date.fromtimestamp(ts)
            if not day2id.has_key(da):
                day2id[da] =  [weiboid]
            else:
                day2id[da].append(weiboid)
        result = []
        daypoint = max(day2id.keys())
        day_list = [daypoint,daypoint-datetime.timedelta(days=1),daypoint-datetime.timedelta(days=2),
                    daypoint-datetime.timedelta(days=3),daypoint-datetime.timedelta(days=4),
                    daypoint-datetime.timedelta(days=5),daypoint-datetime.timedelta(days=6)]
        for da in day_list:
            if da in day2id.keys():
                result.append([str(da),len(day2id[da])])
            else:
                result.append([str(da),0])
        return result
    if timemodule == "day":
        day2id = {}
        for s in statuses:
            ts = s['ts']
            weiboid = s['_id']
            da = date.fromtimestamp(ts)
            if not day2id.has_key(da):
                day2id[da] =  [weiboid]
            else:
                day2id[da].append(weiboid)
        r = sorted(day2id.iteritems(),key=lambda(k,v):len(v))
        maxdate = r[len(r)-1][0]
        raw = {}
        timestr = str(maxdate) + " 00:00:00"
        timestamp = time.mktime(time.strptime(timestr,'%Y-%m-%d %H:%M:%S'))
        time_list = [timestamp,timestamp+3600*4,timestamp+3600*8,timestamp+3600*12,timestamp+3600*16,timestamp+3600*20,timestamp+3600*24]
        for s in statuses:
            ts = s['ts']
            weiboid = s['_id']
            da = date.fromtimestamp(ts)
            if da == maxdate:
                for i in range(0,(len(time_list)-1)):
                    if s['ts'] >= time_list[i] and s['ts'] < time_list[i+1]:
                        if not raw.has_key(i):
                            raw[i] =  [s['ts']]
                        else:
                            raw[i].append(s['ts'])
        result = sorted(raw.iteritems(),key=operator.itemgetter(0))
        results = []
        for re in result:
            results.append(len(re[1]))
        return [str(maxdate),results]

def getProvince(place):
    try:
        place_str = place.split(' ')
        province = place_str[0]
        if province == u"海外" or province == u"其他":
            return -1
        else:
            return province
    except Exception, e:
        print "get province",e
        return -1
    
if __name__ == '__main__': pass
