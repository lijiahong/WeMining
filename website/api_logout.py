#-*- coding:utf-8 -*-

import web

from weibo import APIClient
from config import getDB, APP_KEY, APP_SECRET, CALLBACK_URL

urls = ('/logout', )

class handler():
    def GET(self):
        web.setcookie('WEIBO_UID', '', expires=-1, domain='.buaa.edu.cn', secure=False)
        web.redirect('/')
