#-*- coding:utf-8 -*-

from config import getDB

urls = ('/api/spider/count.json', )

db = getDB()

class handler():
    def GET(self):
        return '%d;%d' % (db.statuses.find().count(), db['target_statuses'].find().count())
