# -*- coding: utf-8 -*-

'''mapweibo首页
'''

import web

urls = ('/mapweibo/trendview', '/mapweibo/trendview/')
render = web.template.render('./templates/')

class handler():
    def GET(self):
        return render.trendview()
