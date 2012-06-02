#-*- coding=utf-8 -*-

'''热门话题微博mid队列
'''

import redis

class MidQueue():
    def __init__(self, queue_name='topic_mid_queue'):
        self.r = redis.Redis()
        self.queue_name = queue_name

    def pop(self):
        p = self.r.blpop(self.queue_name)[1].split(':')
        mid = info = None
        try:
            mid, info = p[0], p[1]
        except:
            pass
        return mid, info

    def push(self, mid, info):
        self.r.rpush(self.queue_name, '%s:%s' % (mid, info))

    def empty(self):
        if not self.r.llen(self.queue_name):
            return True
        else:
            return False

def main():
    job_list = MidQueue()
    job_list.push(u'ykBUBdjEm:鏂囧寲')
    print job_list.pop()

if __name__ == '__main__': main()
