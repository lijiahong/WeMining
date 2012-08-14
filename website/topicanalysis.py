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
from config import getUser

search = Search()

render = web.template.render('./templates/', base='layout')

urls = ('/topicweibo/analysis', )

class handler():
    def GET(self):
        uid = web.cookies().get('WEIBO_UID')
        screen_name, profile_image_url, access_token, expires_in = getUser(uid)
        form = web.input(topic=None, json=None, public=None, page=None, history=None)
        topic = form.topic
        json = form.json
        public = form.public
        page = form.page
        history = form.history
        if topic and json and public:
            if not page:
                page = 1
            if not history:
                return fetchPublicStatuses(topic, page)
            else:
                return fetchPublicStatuses(topic, page, model='history')
        elif topic and json:
            if not history:
                return analysis_data(topic)
            else:
                return analysis_data(topic, model='history')
        elif topic:
            return render.topicanalysis(screen_name, profile_image_url)
        else:
            return render.demo(screen_name, profile_image_url)

def fetchPublicStatuses(topic, page, model='hot'):
    keywords = cut(topic)
    current_ts = int(time.time())
    start = 0
    #start = current_ts - 2*7*24*60*60
    end = current_ts
    if model == 'hot':
        statuses = search.query(keywords, limit=500, order=-1, ts={'$gte': start, '$lte': end})['results']
    else:
        statuses = search.query(keywords, limit=500, order=1, ts={'$gte': start, '$lte': end})['results']
    results = []
    for status in statuses:
        hashtags = status["hashtags"]
        hashtags_str = ""
        if hashtags:
            hashtags_str = ','.join(hashtags)
        results.append([str(date.fromtimestamp(status["ts"])), status["location"], status["name"], status["text"], hashtags_str])    
    return json.dumps(results)

def analysis_data(topic, model='hot'):
    keywords = cut(topic)
    current_ts = int(time.time())
    start = 0
    #start = current_ts - 2*7*24*60*60
    end = current_ts
    if model == 'hot':
        results = search.query(keywords, emotion=True, limit=10000, order=-1, ts={'$gte': start, '$lte': end})
    else:
        results = search.query(keywords, emotion=True, limit=10000, order=1, ts={'$gte': start, '$lte': end})
    statuses = results['results']
    emotions = results['emotions']
    timedist = time_dist(statuses)
    china_map_count, city_sorted = map_count(statuses)
    mood_timeline = mood_timeline_f(statuses, emotions)
    mood_location = mood_location_f(statuses, emotions, city_sorted)
    random_statuses = random_statuses_f(statuses)
    return json.dumps({'timedist': timedist,
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
    #color = ['#000079', '#0f1486', '#1e2893', '#2d3ca1', '#3c51ae', '#4b65bc', '#5a79c9', '#698ed6', '#78a2e4', '#87b6f1', '#96cafe']
    color = ['#2873AC', '#29AC80', '#51B133', '#FFD914', '#FD8D24', '#FF5B25']
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
            if total_count:
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
    city_sorted = [(city, [0, 0, 0]) for city, count in city_sorted]
    return data, city_sorted

def ts2date(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

def date2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

def location_count(statuses, emotions, city_sorted=None):
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
        total = sum(arr)*1.0
        for i in range(len(arr)):
            if city_sorted:
                for c, e in city_sorted[:10]:
                    if c == city:
                        if most[i] < arr[i]/total:
                            most_city[i] = city
                            most[i] = arr[i]/total
            else:
                if most[i] < arr[i]:
                    most_city[i] = city
                    most[i] = arr[i]
    return {'count': count, 'most': most_city}

def mood_location_f(statuses, emotions, city_sorted):
    dt = {}
    location_emotion_tmline = []
    for status, emotion in zip(statuses, emotions):
        for city, emotions_list in city_sorted:
            if city == status['location'].split(' ')[0]:
                emotions_list[emotion-1] += 1
        date = ts2date(status['ts'])
        if date not in dt:
            dt[date] = {'statuses': [], 'emotions': []}
        dt[date]['statuses'].append(status)
        dt[date]['emotions'].append(emotion)
    total_data = location_count(statuses, emotions)
    total_data_2 = location_count(statuses, emotions, city_sorted=city_sorted)
    total_most = [total_data['most'], total_data_2['most']]
    dt = sorted(dt.iteritems(), key=lambda(k, v): date2ts(k), reverse=True)
    for date, d in dt:
        data = location_count(d['statuses'], d['emotions'])
        count = data['count']
        most = data['most']
        location_emotion_tmline.append([date, most])
    return {'tmline': location_emotion_tmline, 'total_most': total_most, 'province_emotion_dist': city_sorted}

def mood_timeline_f(statuses, emotions):
    em_tmdict = {}
    em_tmline = []
    for status, emotion in zip(statuses, emotions):
        day = date.fromtimestamp(status['ts'])
        if day not in em_tmdict:
            em_tmdict[day] = [emotion]
        else:
            em_tmdict[day].append(emotion)
    for day in em_tmdict:
        total = len(em_tmdict[day])*1.0
        sad = 0
        angry = 0
        happy = 0
        for emotion in em_tmdict[day]:
            if emotion == 1:
                sad += 1
            elif emotion == 2:
                angry += 1
            elif emotion == 3:
                happy += 1
        em_tmline.append([str(day), sad/total, angry/total, happy/total])
    return em_tmline

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

def time_dist(statuses, daypoint=None):
    result = []
    if not len(statuses):
        return result
    day2id = {}
    for s in statuses:
        ts = s['ts']
        weiboid = s['_id']
        da = date.fromtimestamp(ts)
        if not day2id.has_key(da):
            day2id[da] =  [weiboid]
        else:
            day2id[da].append(weiboid)
    daypoint = min(day2id.keys())
    day_list = [daypoint]
    i = 1
    while daypoint+datetime.timedelta(days=i) <= date.today():
        day_list.append(daypoint+datetime.timedelta(days=i))
        i += 1
    for da in day_list:
        if da in day2id.keys():
            result.append([str(da),len(day2id[da])])
        else:
            result.append([str(da),0])
    return result

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
