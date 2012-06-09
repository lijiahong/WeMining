# -*- coding: utf-8 -*-

'''测试Web服务器性能
'''

import urllib
import threading
import time

class RequestThread(threading.Thread):
    def __init__(self, url):
        self.url = url
        self.success_count = 0
        self.stoped = False
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if not self.stoped:
                res = urllib.urlopen(self.url)
                if res.getcode() == 200:
                    self.success_count += 1
            else:
                break
URL = 'http://127.0.0.1/count'
count = 100
threads = [RequestThread(URL) for i in range(count)]

start_time = time.time()
for t in threads:
    t.setDaemon(True)
    t.start()

word = ''
while True:
    word = raw_input("enter q to quit:")
    if word == "q":
        for t in threads:
            t.stoped = True
        break
    else:
        time_span = time.time() - start_time
        all_count = 0
        for t in threads:
            all_count += t.success_count
        print "%s Request/Second" % str(all_count / time_span)
