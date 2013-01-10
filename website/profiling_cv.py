# -*- coding: utf-8 -*-

'''网民分类展示页面
'''

import web

urls = ('/profile/cv', )
render = web.template.render('./templates/')

class handler():
    def GET(self):
        return render.profiling_cv()
    
