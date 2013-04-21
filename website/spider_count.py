#-*- coding:utf-8 -*-

from config import getReadonlyDB

urls = ('/api/spider/count.json', )

db = getReadonlyDB('master_timeline')

class handler():
    def GET(self):
        return '%d;%d' % (db.master_timeline_weibo.find().count(), db['master_timeline_user'].find().count())
