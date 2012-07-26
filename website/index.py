#-*- coding:utf-8 -*-

import web
import time

from config import getDB

render = web.template.render('./templates/')

urls = ('/', )

db = getDB()

class handler():
    def GET(self):
        screen_name = None
        profile_image_url = None
        uid = web.cookies().get('WEIBO_UID')
        if uid:
            user = db['weibo_users'].find_one({'_id': uid})
            if user:
                try: 
                    if user['expires_in'] > time.time():
                        screen_name = user['screen_name']
                        profile_image_url = user['profile_image_url']
                except KeyError:
                    pass
        return render.index(screen_name, profile_image_url)
