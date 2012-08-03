#-*- coding:utf-8 -*-

import web

from config import getUser, APP_KEY, APP_SECRET, CALLBACK_URL
from weibo import APIClient

render = web.template.render('./templates/', base='layout')

urls = ('/topicweibo/', '/topicweibo')

class handler():
    def GET(self):
        uid = web.cookies().get('WEIBO_UID')
        screen_name, profile_image_url, access_token, expires_in = getUser(uid)
        user_trends = None
        if uid and access_token:
            user_trends = []
            client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
            client.set_access_token(access_token, expires_in)
            user_trends = self.get_trends(client, uid)
        return render.topicweibo(screen_name, profile_image_url, user_trends)

    def get_trends(self, client, uid):
        trends = []
        res = client.trends(uid=uid, count=10)
        for trend in res:
            trends.append([trend['hotword'], trend['num']])
        return trends
