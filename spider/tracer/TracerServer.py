#-*- coding:utf-8 -*-


import web
import json
from queues import MidQueue


urls = (
    '/htopic/(.*)', 'HotTopic',
)
job_list = MidQueue()


class HotTopic:
    def GET(self, string):
        mid = info = None
        try:
            mid, info = string.split('@')
        except:
            pass
        if mid and info:
            job_list.push(mid, info)
            return json.dumps({'status': 'ok'})
        return json.dumps({'status': 'error'})

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
            
