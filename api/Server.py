#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''分布式API抓取服务器
'''

import logging
import sys
import pymongo
import eventlet
import time
import json
import random

import sys
sys.path.append('..')

import Queue
import threading

from spider.config import getDB
from queues import UidQueue

import scws
s = scws.Scws()
s.set_charset('utf-8')
s.set_dict('/usr/local/scws/etc/dict.utf8.xdb',scws.XDICT_MEM)
s.add_dict('/usr/local/scws/etc/dict_cht.utf8.xdb',scws.XDICT_MEM)
s.add_dict('/opt/WeMining/tokenizer/userdic.txt',scws.XDICT_TXT)
s.set_rules('/usr/local/scws/etc/rules.utf8.ini')
s.set_ignore(1)
stopwords = set([line.strip('\r\n') for line in file('/opt/WeMining/tokenizer/ext_stopword.dic')])

#分词模块
def cut(text,f=None):
    global s, stopwords
    if f:
        return [token[0].decode('utf-8') for token in s.participle(text.encode('utf-8')) if token[0] not in stopwords and token[1] in f]
    else:
        return [token[0].decode('utf-8') for token in s.participle(text.encode('utf-8')) if token[0] not in stopwords]

HOST = '0.0.0.0'
PORT = 9001

uid_queue = UidQueue()
data_queue = Queue.Queue()


def addNewUser():
    '''添加redis队列中Mongodb数据库中新添加的uid
    '''
    global uid_queue
    db = getDB()
    users = db.users.find({'last_modify': {'$gt': 0}, 'pages': {'$gt': 30}})
    us = []
    for user in users:
        us.append(int(user['_id']))
    random.shuffle(us)
    print '%s users will push to uid queue...' % len(us)
    for uid in us:
        uid_queue.add(uid)
    print 'push ok.'


class DataConsumerThread(threading.Thread):
    '''将数据队列的数据存入数据库
    '''
    def __init__(self, db=None, data_queue=None):
        self.db = db
        self.data_queue = data_queue
        self.stoped = False
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                if not self.data_queue.empty():
                    data = self.data_queue.get()
                    if 'user_statuses' in data:
                       for status in data['user_statuses']:
                          exist = self.db['user_statuses'].find({'_id': status['_id']}).count()
                          if not exist:
                              text = status['text']
                              try:
                                  text += status['repost']['text']
                              except KeyError:
                                  pass
                              text_list = cut(text)
                              status['_keywords'] = text_list
                              self.db['user_statuses'].insert(status)
                else:
                    if self.stoped:
                        break
                    else:
                        time.sleep(0.5)
            except Exception, e:
                print e
                continue

def handle(fd, address):
    global data_queue
    global uid_queue
    db = getDB()
    print 'connection accepted from %s:%s' % address
    while True:
        data = fd.readline()
        if not data:
            break
        r = json.loads(data)
        if 'action' in r:
            action = r['action']
        else:
            fd.write(json.dumps({'error': 'wrong instructions'})+'\r\n')
            fd.flush()
        if action == 'postdata':
            try:
                data_queue.put(r['data'])
                fd.write(json.dumps({'status': 'ok'})+'\r\n')
            except:
                fd.write(json.dumps({'error': 'bad request data'})+'\r\n')
            fd.flush()
        elif action == 'getuid':
            if not uid_queue.empty():
                uid = uid_queue.pop()
                fd.write(json.dumps({'uid': uid})+'\r\n')
            else:
                fd.write(json.dumps({'error': 'uid queue empty'})+'\r\n')
            fd.flush()
        else:
            fd.write(json.dumps({'error': 'wrong instructions'})+'\r\n')
            fd.flush()
    print 'end connection %s:%s' % address

def main():
    global uid_queue
    global data_queue
    db = getDB()
    dct = DataConsumerThread(db=db, data_queue=data_queue)
    dct.setDaemon(True)
    dct.start()
    try:
        if sys.argv[1] == 'new':
            addNewUser()
    except IndexError:
        pass
    server = eventlet.listen((HOST, PORT))
    pool = eventlet.GreenPool()
    while True:
        try:
            new_sock, address = server.accept()
            pool.spawn_n(handle, new_sock.makefile('rw'), address)
        except (SystemExit, KeyboardInterrupt):
            break
        except Exception, e:
            print 'Server Error: %s' % e

    dct.stoped = True

if __name__ == '__main__': 
    #main()
    addNewUser()
