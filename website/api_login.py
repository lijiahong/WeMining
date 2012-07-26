#-*- coding:utf-8 -*-

import web

from weibo import APIClient
from config import getDB, APP_KEY, APP_SECRET, CALLBACK_URL

urls = ('/login', )

class handler():
    def GET(self):
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        url = client.get_authorize_url()
        web.redirect(url)
