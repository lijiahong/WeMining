# -*- coding: utf-8 -*-

'''单个网民画像页面
'''

import web

urls = ('/profile/person', )
render = web.template.render('./templates/')

class handler():
    def GET(self):
        return render.profiling_person()
    
