# -*- coding:utf-8 -*-

'''analysis users in hot topics
'''

import os
import codecs

files = [x for x in os.listdir('.') if x.endswith('.txt')]
user_topic = {}
for f_name in files:
    f = codecs.open(f_name, 'r', encoding='utf-8')
    data = f.readlines()
    f.close()
    if len(data) > 1:
        mid, category = data[0].split()
        data = data[1:]
        for line in data:
            try:
                uid, name, gender, location, weibo_count, follower_count, followee_count, ts = line.split()
            except:
                pass
            if uid not in user_topic.keys():
                user_topic[uid] = [mid]
            else:
                mids = user_topic[uid]
                if mid not in mids:
                    mids.append(mid)

user_topic_sorted = sorted(user_topic.iteritems(), key=lambda (k, v): len(v))
for uid, mids in user_topic_sorted:
    if len(mids) > 1:
        print uid
            

