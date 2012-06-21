#-*- coding:utf-8 -*-

from config import db

urls = ('/count/.*', )

class handler():
    def GET(self):
        return '%d;%d' % (db.statuses.find().count(), db['target_statuses'].find().count())
