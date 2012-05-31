import redis
import pymongo

r = redis.Redis()

connection = pymongo.Connection()
db = connection.admin
db.authenticate('root', 'root')
db = connection.weibo

#users = db.users.find({'last_modify': {'$gt':0}})
#user_num = users.count()
#print user_num
#for user in users:
#    uid = int(user['_id'])
#    r.srem('uid_queue', uid)
used = ['friendships', 'statuses', 'period', 'test', 'emotion_test', 'users']
for collection_name in db.collection_names():
    if collection_name in used:
        print collection_name, 'not remove'
    if collection_name not in used:
        print collection_name, 'removed'
        try:
            db.drop_collection(collection_name)
        except:
            pass
