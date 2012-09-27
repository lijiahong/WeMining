#-*- coding:utf-8 -*-

from config import getDB

urls = ('/api/spider/count.json', )

db = getDB()

class handler():
    def GET(self):
        return '%d;%d' % (db.user_statuses.find().count(), db['user_statuses'].find().count())
