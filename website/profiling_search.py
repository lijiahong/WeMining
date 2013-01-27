# -*- coding: utf-8 -*-

'''网民搜索与分类展示
'''

import web

urls = ('/profile/search', )
render = web.template.render('./templates/')

class handler():
    def GET(self):
        return render.profiling_search()
    
