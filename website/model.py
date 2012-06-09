# -*- coding: UTF-8 -*-
import pymongo
from pymongo import Connection
import json
import re
import time
import datetime
import urllib
from simplesearch import WeiboSearch

DB_USER_NAME = 'root'
DB_USER_PWD = 'root'
connection = pymongo.Connection()#"219.224.135.60",27017)
db = connection.admin
db.authenticate(DB_USER_NAME, DB_USER_PWD)
db = connection.weibo

location2latlon = {}
for p in db.location.find():
    location2latlon[p['location'].encode('utf-8')] = p['latlon']
locations = location2latlon.keys()
    
def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o

class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value
        
#def formatLocation(location):
#    location = re.sub(r' ', ',', location)
#    return location

def getLatLon(location):
    try:
        tokens = location.split(' ')
        if len(tokens) == 1:
            province, district = tokens[0], None
        elif len(tokens) == 2:
            province, district = tokens[0], tokens[1]
        if province == u'其他'.encode('utf-8'):
            return 'null'
    except Exception, e:
        print e
        return 'null'
    if not db.location.find({'location': location}).count():
        if province == u'海外'.encode('utf-8'):
            if not district or district == u'其他'.encode('utf-8'):
                return 'null'
            q = location
        else:
            q = (u'中国'.encode('utf-8')+location)
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
        time.sleep(0.5)
    else:
        latlon = db.location.find_one({'location': location})['latlon']
    return latlon

def getTime(topic):
    timearr = db['statuses'].find({'_keywords':  topic}, sort=[('ts', pymongo.ASCENDING)], fields=['ts'])
    for a in timearr:
        print a
    


def getTopics(topic,starttime,endtime):
    global locations, location2latlon
    start = time.time()
    """
    fields=['location','ts','repost.location','repost._md5']
    total_num = db['statuses'].find({'_keywords':  topic}).count()
    select_num = int(total_num/10)
    results = db['statuses'].find({'_keywords':  topic, 'ts':{"$gte":starttime,"$lte":endtime}}, sort=[('ts', pymongo.ASCENDING)], fields=fields)
    """
    search = WeiboSearch()
    starttime = str(starttime)
    endtime = str(endtime)
    results = search.query(begin=starttime,end=endtime,qtype='lh',keywords=[topic],hashtags=[])
    print time.time()-start
    result_list = []
    print results[0]
    for status in results:
        if status['repost_location'] != '':
            t_location = status['location']
            f_location = status['repost_location']
            if t_location == '' or f_location == '':
                continue
            if f_location not in locations:
                location2latlon[f_location] = getLatLon(f_location)
                locations = location2latlon.keys()
            if t_location not in locations:
                location2latlon[t_location] = getLatLon(t_location)
                locations = location2latlon.keys()
            result_list.append({'original': 0,
                                'release_time': status['timestamp'],
                                'forward_address': f_location,
                                'forward_latlng': location2latlon[f_location],
                                'release_address': t_location,
                                'release_latlng': location2latlon[t_location]
                })
        else:
            lt = status['location']
            if lt == '':
                continue
            if lt not in locations:
                location2latlon[lt] = getLatLon(lt)
                locations = location2latlon.keys()
            result_list.append({'original': 1,
                                'release_time': status['timestamp'],
                                'release_address': lt,
                                'release_latlng': location2latlon[lt]
                                })
    #return json.dumps(result_list)
    #print result_list
    return result_list

def getCount():
    return db.statuses.find().count()

if __name__ == '__main__':
    print getCount()
    #getTime("雷锋")
    timenow = datetime.datetime.now()
    begin = time.mktime((timenow + datetime.timedelta(days=-180)).timetuple())
    end = time.mktime(timenow.timetuple())

    getTopics(u"薄熙来".encode('utf-8'),begin,end)
