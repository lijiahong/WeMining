#-*- coding:utf-8 -*-

import web

from config import getUser

render = web.template.render('./templates/', base='layout')

urls = ('/topicweibo/', '/topicweibo')

class handler():
    def GET(self):
        uid = web.cookies().get('WEIBO_UID')
        screen_name, profile_image_url, access_token = getUser(uid)
        return render.topicweibo(screen_name, profile_image_url)
