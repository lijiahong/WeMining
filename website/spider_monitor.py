#-*- coding:utf-8 -*-

import web

render = web.template.render('./templates/', )

urls = ('/spider/', )

class handler():
    def GET(self):
        return render.spider()
