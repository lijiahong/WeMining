#-*- coding: utf-8 -*-

'''微博情绪pattern页面
'''

import json
import urllib
import time
import web

render = web.template.render('./templates/')

urls = ('/emotion_pattern/', '/emotion_pattern/')

class handler():
    def GET(self):
        return render.senti_pattern_view()
    def POST(self):
        pass