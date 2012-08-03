#-*- coding:utf-8 -*-

import web
import time

from config import getDB, getUser

render = web.template.render('./templates/')

urls = ('/', )

db = getDB()

class handler():
    def GET(self):
        uid = web.cookies().get('WEIBO_UID')
        screen_name, profile_image_url, access_token, expires_in = getUser(uid)
        return render.index(screen_name, profile_image_url)
