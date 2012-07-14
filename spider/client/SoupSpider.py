#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''新浪微博爬虫
'''

import os
import sys
import time

import math
import md5
import random
import re

import urllib3
import socket

import json

import profile

import threading
import Queue

from _socket import error
from NiceFork import _obj_hook, load_cookies, unix2localtime, smc2unix, clean_html, clean_status
from BeautifulSoup import BeautifulSoup, SoupStrainer
from tokenizer import smallseg

from ConfigParser import ConfigParser
from config import LOGGER, CONFIG_FILE

config = ConfigParser()
config.read(CONFIG_FILE)
try:
    HOST = config.get('server', 'host')
    PORT = config.getint('server', 'port')
    THREAD_NUM = config.getint('number', 'thread')
except Exception, e:
    LOGGER.error('%s Config File Error!' % e)


def recv_line(socket):
    line = socket.recv(1024)
    done = False;
    while not done:
        if re.search('\r\n', line):
            done = True
        else:
            more = socket.recv(1024)
            if not more:
                done = True
            else:
                line += more
    return line


class WeiboURL(object):
    '''根据地址获得微博中的网页 线程安全
    '''
    def __init__(self, passport, proxy):
        user_agent = '''Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us)
                AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4
                Mobile/7B334b Safari/531.21.10'''
        if not passport:
            print 'no passport available, check server have more account.'
            LOGGER.error('no passport available')
        cookie_str = load_cookies(passport)
        self.headers = {'User-Agent': user_agent,
                  'Cookie': cookie_str}
        if proxy:
            print 'use proxy %s' % proxy
            self.http_pool = urllib3.proxy_from_url('http://%s/' % proxy, timeout=5, maxsize=THREAD_NUM*2, headers=self.headers)
        else:
            self.http_pool = urllib3.connection_from_url("http://weibo.cn", timeout=5, maxsize=THREAD_NUM*2, headers=self.headers)

    def urlopen(self, url):
        res = self.http_pool.urlopen('GET', url, headers=self.headers)
        return res.data


class Spider(object):
    '''微博爬虫集成
    '''
    def __init__(self, task):
        self.task = task
        self.spiders = []
        self.socket = socket.socket()
        self.socket.connect((HOST ,PORT))
        #get proxy host and port
        self.socket.sendall(json.dumps({'action': 'getproxy'})+'\r\n')
        res = recv_line(self.socket)
        r = json.loads(res, object_hook=_obj_hook)
        proxy = None
        if hasattr(r, 'error'):
            LOGGER.error(r.error)
        else:
            proxy = r.proxy
        #get weibo account name and password
        self.socket.sendall(json.dumps({'action': 'getpassport'})+'\r\n')
        res = recv_line(self.socket)
        r = json.loads(res, object_hook=_obj_hook)
        passport = None
        if hasattr(r, 'error'):
            LOGGER.error(r.error)
        else:
           passprot = r.passport
        #get black user id list
        self.socket.sendall(json.dumps({'action': 'getblacklist'})+'\r\n')
        res = recv_line(self.socket)
        r = json.loads(res, object_hook=_obj_hook)
        self.balck_list = []
        if hasattr(r, 'error'):
            LOGGER.error(r.error)
        else:
            black_list = r.black_list
            if black_list:
                self.black_list = black_list
        self.socket.close()
        self.client = WeiboURL(passport, proxy)
        self.seg = smallseg.SEG()
        self.stoped = False


    def spider(self, join=False):
        for i in range(THREAD_NUM):
            st = SpiderThread(i, task=self.task, controler=self, client=self.client,
                              tokenizer=self.seg, black_list=self.black_list)
            st.setDaemon(True)
            self.spiders.append(st)
        for spider_thread in self.spiders:
            spider_thread.start()
        if join:
            for spider_thread in self.spiders:
                spider_thread.join()

    def paused(self):
        self.stoped = not self.stoped
    
class SpiderThread(threading.Thread):
    '''单个抓取线程
    '''
    def __init__(self, num, task='random', controler=None, client=None,
                 tokenizer=None, black_list=None):
        self.num = num
        self.task = task
        self.controler = controler
        self.client = client
        self.tokenizer = tokenizer
        self.black_list = black_list
        self.socket = socket.socket()
        threading.Thread.__init__(self)

    def getuid(self):
        self.socket.sendall(json.dumps({'action': 'getuid'})+ '\r\n')
        res = recv_line(self.socket)
        r = json.loads(res, object_hook=_obj_hook)
        if hasattr(r, 'error'):
            LOGGER.error(r.error)
            return None
        else:
            return r.uid, r.pages

    def gettargetuid(self):
        self.socket.sendall(json.dumps({'action': 'gettargetuid'})+'\r\n')
        res = recv_line(self.socket)
        r = json.loads(res, object_hook=_obj_hook)
        if hasattr(r, 'error'):
            LOGGER.error(r.error)
            return None
        else:
            return r.uid

    def getuserinfo(self, **kw):
        try:
            name = kw['name']
        except:
            return None
        self.socket.sendall(json.dumps({'action': 'getuserinfo', 'data': name})+ '\r\n')
        done = false
        res = recv_line(self.socket)
        r = json.loads(res, object_hook=_obj_hook)
        if hasattr(r, 'error'):
            return None
        else:
            return r.user
        
    def postdata(self, **kw):
        try:
            data = kw['data']
        except:
            return None
        self.socket.sendall(json.dumps({'action': 'postdata', 'data': data})+ '\r\n')
        res = recv_line(self.socket)
        r = json.loads(res, object_hook=_obj_hook)
        if hasattr(r, 'error'):
            LOGGER.error(r.error)
            return None
        else:
            return r.status
    
    def request(self, action=None, **kw):
        func = getattr(self, action)
        return func(**kw)
    
    def run(self):
        flag = True
        try:
            self.socket.connect((HOST ,PORT))
        except error:
            print 'connection failed'
            return
        print 'connected to server %s:%s' % (HOST, PORT)
        while flag:
            try:
                if not self.controler.stoped:
                    if self.task == 'random':
                        uid, pages = self.request(action='getuid')
                        self.travel(uid=uid, pages=pages)
                        time.sleep(1)
                    elif self.task == 'target':
                        uid = self.request(action='gettargetuid')
                        self.target_travel(time.time()-24*60*60, uid=uid)
                        time.sleep(1)
                    else:
                        pass
                else:
                    time.sleep(1)
            except Exception, e:
                LOGGER.error('Unhandled Error:%s' % e)
        self.socket.close()
        
    def target_travel(self, ts, uid=None):
        if not uid:
            return None
        if uid in self.black_list:
            return None
        url = 'http://weibo.cn/u/'+uid
        current_page = 1
        home_page_soup = BeautifulSoup(self.client.urlopen(url+'?page=1'))
        try:
            name, verified, gender, location, desc, tags = self._travel_info(uid)
            print 'target spider %d searching uid: %s name: %s...' % (self.num, uid, name)
        except Exception, e:
            LOGGER.error('User %s Info Page Error:%s' % (uid, e))
            return None
        if not name or not gender or not location:
            #user information missed
            LOGGER.error('User %s Info Page Missed' % uid)
            return None
        flag = True
        while flag:
            if current_page > 1:
                home_page_soup = BeautifulSoup(self.client.urlopen(url+'?page='+str(current_page)),
                                               parseOnlyThese=SoupStrainer('div', {'class': 'c'}))
            posts = []
            for status in home_page_soup.findAll('div', {'class': 'c'})[:-2]:
                post = self._getpost(uid, name, gender, location, status)
                if not post:
                    continue
                if post['ts'] < ts:
                    flag = False
                posts.append(post)
                print post['text'].encode(sys.stdout.encoding, 'ingore')
            if len(posts):
                self.request(action='postdata', data={'target_statuses': posts})
            time.sleep(1)
            current_page += 1
        
    def travel(self, uid=None, pages=0):
        if not uid:
            return None
        if uid in self.black_list:
            return None
        old_total_page = pages
        url = 'http://weibo.cn/u/'+uid
        total_page = 1
        home_page_soup = BeautifulSoup(self.client.urlopen(url+'?page=1'))
        try:
            total_page = int(home_page_soup.find('div', {'class':'pa', 'id':'pagelist'}).form.div.\
                             find('input', {'name':'mp'})['value'])
        except Exception, e:
            #no status or status = 1 page
            pass
        if total_page < old_total_page:
            return None
        try:
            name, verified, gender, location, desc, tags = self._travel_info(uid)
            print 'spider %d searching uid: %s name: %s...' % (self.num, uid, name)
        except Exception, e:
            LOGGER.error('User %s Info Page Error:%s' % (uid, e))
            return None
        if not name or not gender or not location:
            #user information missed
            LOGGER.error('User %s Info Page Missed' % uid)
            return None
        for current_page in range(1, total_page-old_total_page+1):
            if current_page > 1:
                home_page_soup = BeautifulSoup(self.client.urlopen(url+'?page='+str(current_page)),
                                               parseOnlyThese=SoupStrainer('div', {'class': 'c'}))
            #print current_page
            people_list = []
            posts = []
            for status in home_page_soup.findAll('div', {'class': 'c'})[:-2]:
                post = self._getpost(uid, name, gender, location, status, people_list=people_list)
                if not post:
                    continue
                print post['text'].encode(sys.stdout.encoding, 'ingore')
                posts.append(post)
            if len(posts):
                self.request(action='postdata', data={'users': people_list, 'statuses': posts})
            time.sleep(0.5)
        fresh_user = {'_id': uid,
                      'name': name,
                      'verified': verified,
                      'gender': gender,
                      'location': location,
                      'desc': desc,
                      'tags': tags,
                      'pages': total_page,
                      'last_modify': int(time.time())}
        self.request(action='postdata', data={'user': fresh_user})

    def _travel_info(self, uid):
        url = 'http://weibo.cn/'+uid+'/info'
        name, verified, gender, location, desc, tags = None, None, None, None, None, None
        home_page_soup = BeautifulSoup(self.client.urlopen(url))
        user_info_div = home_page_soup.findAll('div', {'class': 'c'})
        if len(user_info_div) < 4:
            time.sleep(0.5)
            home_page_soup = BeautifulSoup(self.client.urlopen(url))
            user_info_div = home_page_soup.findAll('div', {'class': 'c'})
            if len(user_info_div) < 4:
                return
        user_info_div  = user_info_div[3]
        for br_tag in user_info_div.contents:
            info_string = br_tag.string
            if info_string:
                rname = re.search(u'昵称:(.+)', info_string)
                if rname:
                    name = rname.group(1)
                    continue
                rverified = re.search(u'认证:(.+)', info_string)
                if rverified:
                    verified = rverified.group(1)
                    continue  
                rgender = re.search(u'性别:(.+)', info_string)
                if rgender:
                    gender = rgender.group(1)
                    continue
                rlocation = re.search(u'地区:(.+)', info_string)
                if rlocation:
                    location = rlocation.group(1)
                    continue
                rdesc = re.search(u'简介:(.+)', info_string)
                if rdesc:
                    desc = rdesc.group(1)
                    continue
        a_tags = user_info_div.findAll('a')[:-1]
        if a_tags:
            tags = []
            for a_tag in a_tags:
                try:
                    b = a_tag.contents[0]
                    tags.append(b)
                except:
                    pass
        return name, verified, gender, location, desc, tags

    def _getuid(self, url):
        home_page_soup = BeautifulSoup(self.client.urlopen(url))
        uid = None
        user_info_div = home_page_soup.find('div', {'class': 'ut'})
        for user_info_div_a in user_info_div.findAll('a'):
            user_info_div_a_result = re.search(r'/(\d+)/info', user_info_div_a['href'])
            if  user_info_div_a_result:
                uid =  user_info_div_a_result.group(1)
                break
        return uid
    
    def _getpost(self, uid, name, gender, location, status, people_list=None):
        weibo_user_url_pattern = r'http://weibo.cn/u/(\d+)\D*'
        try:
            mid = status['id'][2:]
        except Exception, e:
            #no status publish
            return None
        status_divs = status.findAll('div')
        status_divs_count = len(status_divs)
        if status_divs_count == 2:
            #text & repost_text
            div = status_divs[0]
            cmt = div.find('span', {'class': 'cmt'})
            try:
                #some weibo may be deleted
                source_user_a_tag = cmt.contents[1]
                source_user_url = 'http://weibo.cn'+source_user_a_tag['href']
                source_user_name = source_user_a_tag.string
            except:
                return None
            ctt = div.find('span', {'class': 'ctt'})
            source_text = ''
            for ctt_tag in ctt.contents:
                try:
                    source_text += clean_html(ctt_tag.string)
                except:
                    pass
            source_text.strip()
            if not source_text:
                return None
            #print source_user_name+':'+source_text
            re_div = status_divs[1]
            re_text = ''
            for re_tag in re_div.contents[1:-9]:
                try:
                    re_text += clean_html(re_tag.string)
                except:
                    pass
            re_text.strip()
            if not re_text:
                return None
            ct_span = re_div.find('span', {'class': 'ct'})
            if len(ct_span.contents)> 1:
                creat_at = ct_span.contents[0][:-8] #remove &nbsp;来自
                ts = int(smc2unix(creat_at))
                source = ct_span.contents[1].string
            else:
                tokens = ct_span.string.split('&nbsp;')
                ts = int(smc2unix(tokens[0].strip()))
                source = tokens[1][2:].strip()
            content = re_text+' '+source_text
            content, urls, hashtags, emotions = clean_status(content)
            text_list = self.tokenizer.cut(content)
            source_user = self.request(action='getuserinfo', name=source_user_name)
            if source_user:
                print 'RT: %s' % source_user_name
                source_user_uid = source_user['_id']
                source_user_gender = source_user['gender']
                source_user_location = source_user['location']
            else:
                r_source_user_uid = re.search(weibo_user_url_pattern, source_user_url)
                if r_source_user_uid:
                    source_user_uid = r_source_user_uid.group(1)
                else:
                    source_user_uid = self._getuid(source_user_url)
                if source_user_uid and source_user_uid not in self.black_list:
                    pass
                else:
                    LOGGER.error('Repost User Missed')
                    return None
                time.sleep(0.5)
                source_user_name, source_user_verified, source_user_gender, source_user_location, \
                                  source_user_desc, source_user_tags = self._travel_info(source_user_uid)
                if not source_user_name or not source_user_gender or not source_user_location:
                    LOGGER.error('Repost User %s Missed' % source_user_uid)
                    return None
                if people_list:
                    new_user = {'_id': source_user_uid,
                            'name': source_user_name,
                            'verified': source_user_verified,
                            'gender': source_user_gender,
                            'location': source_user_location,
                            'desc': source_user_desc,
                            'tags': source_user_tags,
                            'pages': 0,
                            'last_modify': 0}
                    people_list.append(new_user)
            post = {'_id': mid,
                    'uid': uid,
                    'name': name,
                    'gender': gender,
                    'location': location,
                    'text': re_text,
                    'repost': {'uid': source_user_uid,
                               'name': source_user_name,
                               'gender': source_user_gender,
                               'location': source_user_location,
                               'text': source_text,
                               '_md5': md5.new((source_user_uid+source_text).encode('utf-8')).hexdigest()},
                    'source': source,
                    'ts': ts,
                    'urls': urls,
                    'hashtags': hashtags,
                    'emotions': emotions,
                    '_keywords': text_list}
            #print post['repost']['_md5']
        elif status_divs_count == 1:
            #text
            div = status_divs[0]
            ctt = div.find('span', {'class': 'ctt'})
            source_text = ''
            for ctt_tag in ctt.contents:
                try:
                    source_text += clean_html(ctt_tag.string)
                except:
                    pass
            source_text.strip()
            if not source_text:
                return None
            #print source_text
            ct_span = div.find('span', {'class': 'ct'})
            if len(ct_span.contents)> 1:
                creat_at = ct_span.contents[0][:-8] #remove &nbsp;来自
                ts = int(smc2unix(creat_at))
                source = ct_span.contents[1].string
            else:
                tokens = ct_span.string.split('&nbsp;')
                ts = int(smc2unix(tokens[0].strip()))
                source = tokens[1][2:].strip()
            #print source, ts
            content = source_text
            content, urls, hashtags, emotions = clean_status(content)
            text_list = self.tokenizer.cut(content)
            post = {'_id': mid,
                    'uid': uid,
                    'name': name,
                    'gender': gender,
                    'location': location,
                    'text': source_text,
                    'source': source,
                    'ts': ts,
                    'urls': urls,
                    'hashtags': hashtags,
                    'emotions': emotions,
                    '_keywords': text_list,
                    '_md5': md5.new((uid+source_text).encode('utf-8')).hexdigest()}
        else:
            return None
        return post

def main():
    try:
        task = sys.argv[1]
    except IndexError:
        task = 'random'
    s = Spider(task)
    s.spider(join=True)

if __name__ == '__main__':
    #profile.run('main()')
    main()
