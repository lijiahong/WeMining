#-*- coding=utf-8 -*-

'''热门话题微博mid队列
'''

class MidQueue():

    def __init__(self):
        import Queue
        self.queue = Queue.Queue()
        self.queue.put(u'ykBUBdjEm:娱乐')

    def pop(self):
        p = self.queue.get().split(':')
        mid = info = None
        try:
            mid, info = p[0], p[1]
        except:
            pass
        return mid, info

    def push(self, mid, info):
        self.queue.put('%s:%s' % (mid, info))

    def empty(self):
        return self.queue.empty()
