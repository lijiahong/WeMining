#-*- coding:utf-8 -*-

'''Sina Weibo hot topics tweets id queues
'''

import redis
from redis.exceptions import WatchError

class MidQueue():
    def __init__(self, queue_name='topic_mid_queue', hash_name='topic_mid_hash'):
        self.r = redis.Redis()
        self.queue_name = queue_name
        self.hash_name = hash_name

    def pop(self):
        queue_name, string = self.r.blpop(self.queue_name)
        string = string.decode('utf-8')
        p = string.split(':')
        mid = info = None
        try:
            mid, info = p[0], p[1]
        except:
            pass
        return mid, info

    def push(self, mid, info):
        with self.r.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(self.hash_name)
                    count = pipe.hget(self.hash_name, mid)
                    if not count:
                        pipe.multi()
                        pipe.hset(self.hash_name, mid, 1)
                        pipe.rpush(self.queue_name, '%s:%s' % (mid, info))
                        pipe.execute()
                    else:
                        pipe.multi()
                        pipe.hincrby(self.hash_name, mid, 1)
                        pipe.execute()
                    break
                except WatchError:
                    continue

    def empty(self):
        if not self.r.llen(self.queue_name):
            return True
        else:
            return False

def main():
    job_list = MidQueue()
    job_list.push(u'ykBUBdjEm', u'culure')
    print job_list.pop()

if __name__ == '__main__': main()
