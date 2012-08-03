#-*- coding:utf-8 -*-

import pymongo
import web
import time

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

def getUser(uid):
    '''获得指定uid的用户信息
    '''
    db = getDB()
    screen_name = None
    profile_image_url = None
    access_token = None
    expires_in = None
    if uid:
        user = db['weibo_users'].find_one({'_id': uid})
        if user:
            try:
                expires_in = user['expires_in']
                if expires_in > time.time():
                    screen_name = user['screen_name']
                    profile_image_url = user['profile_image_url']
                    access_token = user['access_token']
            except KeyError:
                pass
    return screen_name, profile_image_url, access_token, expires_in
