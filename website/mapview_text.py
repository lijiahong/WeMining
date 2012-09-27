# -*- coding: utf-8 -*-

'''获取mapview微博文本及其他信息接口
'''

import json
import re
import time
import urllib
from datetime import date
import web
import pymongo

from config import getDB

urls = ('/mapweibo/mapview/text', )
db = getDB()

class handler():
    def GET(self):
        form = web.input(idlist=None, module=None, collection=None)
        if form.idlist:
            data = getInfoById(form.idlist, form.collection)
            if not form.module:
                return json.dumps(data[0])
            else:
                return json.dumps(data[1])

location2latlon = {}
for p in db.location.find():
    location2latlon[p['location']] = p['latlon']
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

def getLatLon(location):
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
        time.sleep(0.5)
    else:
        latlon = db.location.find_one({'location': location})['latlon']
    return latlon

def detailInfo(topic,starttime,endtime,location):
    global locations, location2latlon
    start = time.time()
    fields=['uid','_id','ts','location','name','text','hashtags']
    results = db['statuses'].find({'ts':{"$gte":starttime,"$lte":endtime}, '_keywords':  topic,  'location': { "$regex": location + '.*', "$options": 'i' }}, sort=[('ts', pymongo.ASCENDING)], fields=fields)
    #print 'timespend',time.time()-start
    result_list = []
    #print results[0]
    for status in results:
        post_status = u'转发'
        if 'repost' in status.keys():
            post_status = u'转发'
        else:
            post_status = u'原创'
        hashtags_str = ""
        hashtags_list = status['hashtags']
        for h in hashtags_list:
            hashtags_str = hashtags_str + h + "," 
        result_list.append([status['uid'],status['_id'],str(date.fromtimestamp(status['ts'])),status['location'],status['name'],post_status,status['text'],hashtags_str])
    return result_list

def getInfoById(idlist,collection):
    global locations, location2latlon
    start = time.time()
    fields=['uid','_id','ts','location','name','text','hashtags','repost.location']
    ids = idlist.split(" ")
    if collection == "statuses":
        results = db['statuses'].find({'_id':{"$in":ids}}, sort=[('ts', pymongo.ASCENDING)], fields=fields)
    else:
        results = db['user_statuses'].find({'_id':{"$in":ids}}, sort=[('ts', pymongo.ASCENDING)], fields=fields)
    #print 'timespend',time.time()-start
    result_list = []
    timeline = []
    timeline_hash = {}
    text = []
##    print results[0]
    for status in results:
        post_status = u'转发'
        if 'repost' in status.keys():
            post_status = u'转发'
        else:
            post_status = u'原创'
        hashtags_str = ""
        hashtags_list = status['hashtags']
        if hashtags_list != None:
            for h in hashtags_list:
                hashtags_str = hashtags_str + h + ","
        text.append([str(status['uid']),status['_id'],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(status['ts']))),status['location'],status['name'],post_status,status['text'],hashtags_str])
        #timeline.append([status['ts'],1])
        ts = int(status['ts']*1000)
        if ts not in timeline_hash.keys():
            timeline_hash[ts] = 1
        else:
            num = timeline_hash[ts]
            timeline_hash[ts] = num + 1
    timeline = sorted(timeline_hash.iteritems(),key=lambda(k,v):k)
    result_list = [text,timeline]
    return result_list
    
        
    

def getCount():
    return db.statuses.find().count()

if __name__ == '__main__':
    detailInfo(u"薄熙来",1331084340.0,1333854240.0,u"北京")
    #print getCount()
