#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''爬虫状态监控服务器
'''

import web
import model

urls = (
    '/count/.*', 'Count',
)
    
class Count:
    def GET(self):
        return model.getCount()
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

