#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''分布式爬虫中央控制器
'''

import pymongo
#import redis
import eventlet

import threading
import Queue

import os
import sys
sys.path.append("..")

import time
import random
import re
import json


from config import LOGGER, HOST, PORT, getDB
from clean import removeModifiedUser, addNewUser
from queues import UidQueue, TargetUidList, UidBlackList, ProxyHash, PassportHash
        
        
#任务队列
uid_queue = UidQueue()
target_uid_queue = TargetUidList()
black_list = UidBlackList()
proxy_hash = ProxyHash()
passport_hash = PassportHash()
data_queue = Queue.Queue()


class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o


class DataConsumerThread(threading.Thread):
    '''将数据队列的数据存入数据库
    '''
    def __init__(self, db=None, data_queue=None, uid_queue=None):
        self.db = db
        self.data_queue = data_queue
        self.uid_queue = uid_queue
        self.stoped = False
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                if not self.data_queue.empty():
                    data = self.data_queue.get()
                    if hasattr(data, 'target_statuses'):
                       for status in data.target_statuses:
                          exist = self.db['target_statuses'].find({'_id': status['_id']}).count()
                          if not exist:
                              self.db['target_statuses'].insert(status)
                    if hasattr(data, 'statuses'):
                        posts = []
                        for status in data.statuses:
                            exist = self.db.statuses.find({'_id': status['_id']}).count()
                            if not exist:
                                posts.append(status)
                        if len(posts):
                            self.db.statuses.insert(posts)
                    if hasattr(data, 'users'):
                        for user in data.users:
                            exist = self.db.users.find_one({'_id': user['_id']})
                            if not exist:
                                self.users.insert(user)
                    if hasattr(data, 'user'):
                        self.db.users.save(data.user)
                else:
                    if self.stoped:
                        break
                    else:
                        time.sleep(0.5)
            except Exception, e:
                LOGGER.error(e)
                continue


def handle(fd, address):
    global data_queue
    global uid_queue
    global target_uid_queue
    global black_list
    global proxy_hash
    global passport_hash
    db = getDB()
    LOGGER.info('connection accepted from %s:%s' % address)
    while True:
        data = fd.readline()
        if not data:
            break
        data = data[:-2]
        r = json.loads(data, object_hook=_obj_hook)
        if hasattr(r, 'action'):
            action = r.action
        else:
            fd.write(json.dumps({'error': 'wrong instructions'})+'\r\n')
            fd.flush()
            break
        if action == 'postdata':
            try:
                data_queue.put(r.data)
                fd.write(json.dumps({'status': 'ok'})+'\r\n')
            except:
                fd.write(json.dumps({'error': 'bad request data'})+'\r\n')
            fd.flush()
        elif action == 'getuid':
            if not uid_queue.empty():
                uid = uid_queue.pop()
                pages = 0
                user = db.users.find_one({'_id': uid})   
                try:
                    pages = user['pages']
                except:
                    pages = 0
                fd.write(json.dumps({'uid': uid, 'pages': pages})+'\r\n')
            else:
                fd.write(json.dumps({'error': 'uid queue empty'})+'\r\n')
            fd.flush()
        elif action == 'getuserinfo':
            try:
                name = r.data
                user = db.users.find_one({'name': name})
                try:
                    u = {'_id': user['_id'], 'gender': user['gender'], 'location': user['location']}
                    fd.write(json.dumps({'user': u})+'\r\n')
                except:
                    fd.write(json.dumps({'error': 'not found'})+'\r\n')
            except:
                fd.write(json.dumps({'error': 'bad request data'})+'\r\n')
            fd.flush()
        elif action == 'gettargetuid':
            uid = target_uid_queue.get()
            if uid:
                fd.write(json.dumps({'uid': uid})+'\r\n')
            else:
                fd.write(json.dumps({'error': 'target uid queue empty'})+'\r\n')
            fd.flush()
        elif action == 'getpassport':
            passport = passport_hash.get(address[0])
            if passport:
                username = passport.split(':')[0]
                passport = passport.split(':')[1]
                fd.write(json.dumps({'passport': {'username': username, 'passport': passport}})+'\r\n')
            else:
                fd.write(json.dumps({'error': 'no free passport'})+'\r\n')
            fd.flush()
        elif action == 'getproxy':
            proxy = proxy_hash.get(address[0])
            if proxy:
                fd.write(json.dumps({'proxy': proxy})+'\r\n')
            else:
                fd.write(json.dumps({'error': 'no free proxy'})+'\r\n')
            fd.flush()
        elif action == 'getblacklist':
            if black_list.empty():
                fd.write(json.dumps({'error': 'empty uid black list'})+'\r\n')
            else:
                fd.write(json.dumps({'black_list': black_list.get()})+'\r\n')
            fd.flush() 
        else:
            fd.write(json.dumps({'error': 'wrong instructions'})+'\r\n')
            fd.flush()
            break
    LOGGER.info('end connection %s:%s' % address)

        
def main():
    global uid_queue
    global data_queue
    db = getDB()

    dct = DataConsumerThread(db=db, data_queue=data_queue, uid_queue=uid_queue)
    dct.setDaemon(True)
    dct.start()

    try:
        if sys.argv[1] == 'update uid queue':
            removeModifiedUser()
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
            LOGGER.error('Server Error: %s' % e)

    dct.stoped = True

if __name__ == '__main__': main()
