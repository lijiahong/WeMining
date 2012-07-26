#-*- coding:utf-8 -*-

import pymongo
import web

#数据库地址和端口
DB_HOST = 'localhost'
DB_PORT = 27017

#数据库账号信息
DB_USER = 'root'
DB_PWD = 'root'

APP_KEY = '3919941931'
APP_SECRET = 'c1fcfc1ca9a92bebef7001fde0415da6'
CALLBACK_URL = 'http://idec.buaa.edu.cn/callback'

def getDB():
    '''获取数据库对象
    '''
    connection = pymongo.Connection(DB_HOST, DB_PORT)
    db = connection.admin
    db.authenticate(DB_USER, DB_PWD)
    return connection.weibo
