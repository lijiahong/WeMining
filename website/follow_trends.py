#-*- coding:utf-8 -*-

import web
import time
import urllib
import json

from weibo import APIClient
from config import getDB, getUser, APP_KEY, APP_SECRET, CALLBACK_URL

urls = ('/topicweibo/followtrends', )

db = getDB()

class handler():
    def GET(self):
        uid = web.cookies().get('WEIBO_UID')
        screen_name, profile_image_url, access_token, expires_in = getUser(uid)
        form = web.input(topic=None)
        topic = form.topic
        if topic and uid and access_token:
            client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
            client.set_access_token(access_token, expires_in)
            res = client.trends__is_follow(trend_name=topic)
            try:
                is_follow = res['is_follow']
                if is_follow == 'false':
                    res = client.post.trends__follow(trend_name=topic)
                    print res
                    topicid = res['topicid']
                    print topicid
                    return json.dumps({'status': 'follow ok'})
                else:
                    return json.dumps({'status': 'is followed'})
            except Exception, e:
                return json.dumps({'status': 'follow error'})
        else:
            return json.dumps({'status': 'need login'})
