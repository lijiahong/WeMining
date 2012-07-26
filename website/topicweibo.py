#-*- coding:utf-8 -*-

import web

render = web.template.render('./templates/')

urls = ('/topicweibo/', )

class handler():
    def GET(self):
        return render.topicweibo()
