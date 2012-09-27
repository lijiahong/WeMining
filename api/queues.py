import redis

class UidQueue(object):
    def __init__(self, queue_name='target_queue'):
        self.r = redis.Redis()
        self.queue_name = queue_name

    def pop(self):
        return self.r.spop(self.queue_name)

    def add(self, value):
        self.r.sadd(self.queue_name, value)

    def empty(self):
       if not self.r.scard(self.queue_name):
           return True
       else:
           return False
