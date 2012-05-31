# -*- coding: utf-8 -*-

import pymongo

DB_USER_NAME = 'root'
DB_USER_PWD = 'root'
connection = pymongo.Connection()
db = connection.admin
db.authenticate(DB_USER_NAME, DB_USER_PWD)
db = connection.weibo

def getCount():
    return '%d;%d' % (db.statuses.find().count(), db['target_statuses'].find().count())

if __name__ == '__main__':
    print getCount()
