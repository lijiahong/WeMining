# -*- coding: UTF-8 -*-
import pymongo
from pymongo import Connection
import json
import random
import datetime
import time
from simplesearch import WeiboSearch

DB_USER_NAME = 'root'
DB_USER_PWD = 'root'
connection = pymongo.Connection()#"219.224.135.60",27017)
db = connection.admin
db.authenticate(DB_USER_NAME, DB_USER_PWD)
db = connection.weibo

def getWeiboNum(topic,filename):
    fields = ['ts','repost.location']
    timenow = datetime.datetime.now()
    begin = str(0.0)
    end = str(time.mktime(timenow.timetuple()))
    search = WeiboSearch()
    results = search.query(begin=begin,end=end,qtype='lh',keywords=[topic],hashtags=[]) 

#    results = db['statuses'].find({'_keywords':  topic}, sort=[('ts', pymongo.ASCENDING)], fields=fields)
    result = []
    time_list = []
    distinct_time_list = []
    data = []
    for re in results:
        time_list.append(re['timestamp'])
        if re['repost_location'] == '':
            data.append([re['timestamp'],0])
        else:
            data.append([re['timestamp'],1])
    distinct_time_list = sorted(set(time_list))
    #print len(time_list)
    print len(distinct_time_list)
    print '1'
    for t in distinct_time_list:
        #print t
        count = 0
        count_fi = 0
        count_re = 0
        for da in data:
            if t == da[0]:
                count = count + 1
                if da[1] == 0:
                    count_fi = count_fi + 1
                if da[1] == 1:
                    count_re = count_re + 1
        
        if count != 0:
            result.append([t*1000,count,count_fi,count_re])
    print len(result)
    if filename == 'total':
        result_total = []
        for re in result:
            result_total.append([re[0],re[1]])
            #print re[0],re[1]
        return json.dumps(result_total)
                                  
    if filename == 'first':
        result_fi = []
        for re in result:
            if re[2] != 0:
                result_fi.append([re[0],re[2]])
        return json.dumps(result_fi)

    if filename == 'repost':
        result_re = []
        for re in result:
            if re[3] != 0:
                result_re.append([re[0],re[3]])
            #print re[0],re[3]
        return 'callback(' + json.dumps(result_re) + ')'

if __name__ == '__main__':
    getWeiboNum(u'雷锋','repost')
