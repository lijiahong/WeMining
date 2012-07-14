#-*- coding:utf-8 -*-

'''queues for spider server and topic tracer.
'''

import redis
from redis.exceptions import WatchError

class UidQueue(object):
    '''Uid Queue, each uid spidering a person's all tweets
    '''
    def __init__(self, queue_name='uid_queue'):
        self.r = redis.Redis()
        self.queue_name = queue_name

    def add(self, value):
        self.r.sadd(self.queue_name, value)

    def pop(self):
        return self.r.spop(self.queue_name)

    def get(self):
        return self.r.srandmember(self.queue_name)   
                       
    def empty(self):
        if not self.r.scard(self.queue_name):
            return True
        else:
            return False

class UidBlackList(object):
    '''Uid that spider don't touch
    '''
    def __init__(self, list_name='uid_black_list'):
        self.r = redis.Redis()
        self.list_name = list_name

    def add(self, value):
        self.r.sadd(self.list_name, value)

    def remove(self, value):
        self.r.srem(self.list_name, value)
        
    def get(self):
        return self.r.smembers(self.list_name)

    def empty(self):
        if not self.r.scard(self.queue_name):
            return True
        else:
            return False 

class ProxyHash(object):
    '''Proxy host:port client ip or 0 if not using
    '''
    def __init__(self, hash_name='proxy_hash'):
        self.r = redis.Redis()
        self.hash_name = hash_name

    def get(self, client):
        proxys = self.r.hkeys(self.hash_name)
        for proxy in proxys:
            if self.r.hget(self.hash_name, proxy) == client:
                return proxy
        for proxy in proxys:
            if not self.r.hget(self.hash_name, proxy):
                self.set(proxy, client)
                return proxy
        return None

    def free(self, proxy):
        self.r.hset(self.hash_name, proxy, '0')
    
    def set(self, proxy, client=None):
        if not client:
            self.r.hset(self.hash_name, proxy, '0')
        else:
            self.r.hset(self.hash_name, proxy, client)

class PassportHash(object):
    '''User name:password client ip or 0 if not using
    '''
    def __init__(self, hash_name='passport_hash'):
        self.r = redis.Redis()
        self.hash_name = hash_name

    def get(self, client):
        passports = self.r.hkeys(self.hash_name)
        for passport in passports:
            if self.r.hget(self.hash_name, passport) == client:
                return passport
        for passport in passports:
            if not self.r.hget(self.hash_name, passport):
                self.set(passport, client)
                return passport
        return None

    def free(self, passport):
        self.r.hset(self.hash_name, passport, '0')
    
    def set(self, passport, client=None):
        if not client:
            self.r.hset(self.hash_name, passport, '0')
        else:
            self.r.hset(self.hash_name, passport, client)

class TargetUidList(object):
    '''Famous and Daren's Uids, a circle list
    '''
    def __init__(self, list_name='uid_list_realtime', hash_name='uid_hash_realtime', index_info='index_info_hash'):
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.r = redis.Redis(connection_pool=pool)
        self.list_name = list_name
        self.hash_name = hash_name
        self.index_info = index_info

        if self.r.hget(index_info, 'left') is None:
            self.r.hset(index_info, 'left', 0)
        if self.r.hget(index_info, 'right') is None:
            #append start uid
            self.r.hset(index_info, 'right', self.count())

    def intappend(self, uid):
        with self.r.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(self.hash_name)
                    count = pipe.hget(self.hash_name, uid)
                    if count is None:
                        pipe.multi()
                        pipe.hset(self.hash_name, uid, 1)
                        pipe.rpush(self.list_name, uid)
                        pipe.hincrby(self.index_info, 'right', 1)
                        pipe.execute()
                    else:
                        pipe.multi()
                        pipe.hincrby(self.hash_name, uid, 1)
                        pipe.execute()
                    break
                except redis.exceptions.WatchError:
                    continue

    def get(self):
        with self.r.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(self.index_info)
                    left = pipe.hget(self.index_info, 'left')
                    right = pipe.hget(self.index_info, 'right')
                    if int(left) < int(right):
                        pipe.multi()
                        pipe.hincrby(self.index_info, 'left', 1)
                        pipe.lindex(self.list_name, left)
                        result = pipe.execute()[1]
                        return result
                    else:
                        #finish
                        pipe.multi()
                        self.r.hset(self.index_info, 'left', 0)
                        self.r.hset(self.index_info, 'right', self.count())
                        pipe.execute()
                        return None
                    break
                except WatchError:
                    continue

    def count(self):
        count = self.r.llen(self.list_name)
        return count

    def left(self):
        left = self.r.hget(self.index_info, 'left')
        return left

    def right(self):
        right = self.r.hget(self.index_info, 'right')
        return right
    
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
