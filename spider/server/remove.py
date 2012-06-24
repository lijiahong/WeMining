#-*- coding:utf-8 -*-

import redis
import pymongo

r = redis.Redis()
connection = pymongo.Connection()
db = connection.admin
db.authenticate('root', 'root')
db = connection.weibo


def removeModifiedUser():
    '''删除redis队列中已经被访问的用户uid
    '''
    users = db.users.find({'last_modify': {'$gt':0}})
    user_num = users.count()
    print user_num
    for user in users:
        uid = int(user['_id'])
        r.srem('uid_queue', uid)
        
        
def cleanCollections():
    '''删除当前数据库中无用的集合 会阻塞数据库当前的其他进程
    '''
    used = ['friendships', 'statuses', 'period', 'test', 'emotion_test', 'users', 'location']
    for collection_name in db.collection_names():
        if collection_name in used:
            print collection_name, 'not remove'
        if collection_name not in used:
            print collection_name, 'removed'
            try:
                db.drop_collection(collection_name)
            except:
                pass
