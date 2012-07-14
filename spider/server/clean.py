#-*- coding:utf-8 -*-

import redis
import pymongo

import sys
sys.path.append("..")

from config import getDB

db = getDB()
r = redis.Redis()

def removeModifiedUser():
    '''删除redis队列中已经被访问的用户uid
    '''
    users = db.users.find({'last_modify': {'$gt':0}})
    user_num = users.count()
    print '%s users will be removed from uid queue' % user_num
    for user in users:
        uid = int(user['_id'])
        r.srem('uid_queue', uid)
    print 'removed completed'
        
def addNewUser():
    '''添加redis队列中Mongodb数据库中新添加的uid
    '''
    users = db.users.find({'last_modify': 0})
    user_num = users.count()
    print '%s users will push to uid queue...' % user_num
    for user in users:
        uid = int(user['_id'])
        r.sadd('uid_queue', uid)
    print 'push ok.'

def cleanCollections():
    '''删除当前数据库中无用的集合 会阻塞数据库当前的其他进程
    '''
    used = ['friendships', 'statuses', 'period', 'test', 'emotion_test', 'users', 'location', 'target_statuses']
    for collection_name in db.collection_names():
        if collection_name in used:
            print collection_name, 'not remove'
        if collection_name not in used:
            print collection_name, 'removed'
            try:
                db.drop_collection(collection_name)
            except:
                pass
