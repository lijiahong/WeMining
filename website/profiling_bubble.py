# -*- coding: utf-8 -*-

'''气泡兔页面
'''

import web

urls = ('/profile/bubble', )
render = web.template.render('./templates/')

class handler():
    def GET(self):
        return render.profiling_bubble()
    
