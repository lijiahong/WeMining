# -*- coding: utf-8 -*-

'''网民群体画像
'''

import web

urls = ('/profile/group', )
render = web.template.render('./templates/')

class handler():
    def GET(self):
        return render.profiling_group()
    
