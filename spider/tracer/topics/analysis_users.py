# -*- coding:utf-8 -*-

'''analysis users in hot topics
'''

import os
import codecs

files = [x for x in os.listdir('.') if x.endswith('.txt')]
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
            #do some analysis

