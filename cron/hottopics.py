#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
sys.path.append('..')

import time

from api.dev_api import APIClient
from spider.config import getDB

def topic(api, type=None):
    if type == 'hour':
        res = api.trends__hourly(source='2298231745',base_app=0)['trends']
    elif type == 'day':
        res = api.trends__daily(source='2298231745',base_app=0)['trends']
    elif type == 'week':
        res = api.trends__weekly(source='2298231745',base_app=0)['trends']
    else:
        return None
    data = []
    for key in res.keys():
        for v in res[key]:
            data.append({'topic': v['query'], 'count': v['amount']})
    return data
    

def main():
    try:
        action = sys.argv[1]
        api = APIClient('linhao1992@gmail.com', 'weibomap', '2298231745')
        present_time = int(time.time())
        data = topic(api, type=action)
        db = getDB()
        if data:
             for d in data:
                 db.topics.save({'topic': d['topic'],
                                 'count': d['count'],
                                 'ts':  present_time,
                                 'type': action})
    except IndexError:
        print 'wrong argument.'
             
if __name__ == '__main__': main()
