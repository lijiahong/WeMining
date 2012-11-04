# -*- coding=utf-8 -*-

import pymongo
import re
import json
import codecs

def make():
    connection = pymongo.Connection()
    db = connection.admin
    db.authenticate('root','root')
    db = connection.weibo

    f = codecs.open(r'sample_tweets.js', 'w', encoding='utf-8')
    count = 0
    f.write('[')
    number = 500000
    for status in db.statuses.find().limit(number):
        count += 1
        if count % 10000 == 0:
            print '%sw tweets' % (count/10000, )
        if count == number:
            f.write('%s' % json.dumps(status))
        else:
            f.write('%s,' % json.dumps(status))
    f.write(']')
    f.close()

def test():
    f = codecs.open(r'sample_tweets.js', 'r', encoding='utf-8')
    tweets = json.load(f)
    for status in tweets:
        print status['text']
    f.close()

if __name__ == '__main__': make()


