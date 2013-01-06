# -*- coding: utf-8 -*-

'''韩德强舆情分析报告
'''

import web

urls = ('/report/', )
render = web.template.render('./templates/')

class handler():
    def GET(self):
        return render.sentiment_report()
    
