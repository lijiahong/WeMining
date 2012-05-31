#!/usr/bin/env python
# -*- coding=utf-8 -*-

'''根据用户关系网获得新用户放入队列
'''

import re
import time
import random
import pymongo
import os
import urllib
import urllib2
import urllib3
import cookielib

from BeautifulSoup import BeautifulSoup, SoupStrainer
from config import LOGGER, WEIBO_USER, WEIBO_PWD, COOKIES_FILE

from queues import UidQueue


def getDB():
    '''获取数据库对象
    '''
    connection = pymongo.Connection()
    db = connection.admin
    db.authenticate('root', 'root')
    return connection.weibo


def load_cookies():
    '''模拟浏览器登录微博,获取cookies字符串
    '''
    mobile = WEIBO_USER
    password = WEIBO_PWD
    user_agent = '''Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us)
            AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4
            Mobile/7B334b Safari/531.21.10'''
    header = {'User-Agent': user_agent}
    cj = cookielib.MozillaCookieJar()
    if os.path.isfile(COOKIES_FILE):
        cj.load(COOKIES_FILE)
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        cookie_list = []
        for cookie in cj:
            if cookie.domain == '.weibo.cn':
                cookie_list.append(str(cookie).split(' ')[1])
            cookie_str = ';'.join(cookie_list)
        return cookie_str
    login_url = '''http://3g.sina.com.cn/prog/wapsite/sso/login.php?ns=1&backURL=http%3A%2F%2Fweibo.cn%2Fdpool%2Fttt%2Fhome.php%3Fs2w%3Dlogin&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt=4&wm=ig_0001_index'''
    res = urllib2.urlopen(urllib2.Request(login_url, headers=header))
    login_html = res.read()
    res.close()
    login_soup = BeautifulSoup(login_html)
    login_form_action = login_soup.find('form')['action']
    vk = pwd = submit = backURL = backTitle = None
    for input_box in login_soup.findAll('input'):
        if input_box['type'] == 'password':
            pwd = input_box['name']
        elif input_box['type'] == 'submit':
            submit = input_box['value']
        elif input_box['type'] == 'hidden':
            if input_box['name'] == 'vk':
                vk = input_box['value']
            elif input_box['name'] == 'backURL':
                backURL = input_box['value']
            elif input_box['name'] == 'backTitle':
                backTitle = input_box['value']
    submit = '%E7%99%BB%E5%BD%95' #登录
    params = urllib.urlencode({'mobile': mobile, pwd: password, 'remember': 'on',
                               'backURL': backURL, 'vk': vk, 'submit': submit})
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    submit_url = 'http://3g.sina.com.cn/prog/wapsite/sso/'+login_form_action
    res = opener.open(urllib2.Request(submit_url, headers=header) ,params)
    redirect_html = res.read()
    res.close()
    redirect_soup = BeautifulSoup(redirect_html)
    redirect_url = redirect_soup.find('a')['href']
    res = opener.open(urllib2.Request(redirect_url, headers=header))
    res.close()
    cj.save(COOKIES_FILE, ignore_discard=True)
    cookie_list = []
    for cookie in cj:
        if cookie.domain == '.weibo.cn':
            cookie_list.append(str(cookie).split(' ')[1])
        cookie_str = ';'.join(cookie_list)
    return cookie_str


class WeiboURL(object):
    '''根据地址获得微博中的网页 线程安全
    '''
    def __init__(self):
        user_agent = '''Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us)
                AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4
                Mobile/7B334b Safari/531.21.10'''

        cookie_str = load_cookies()
        self.headers = {'User-Agent': user_agent,
                  'Cookie': cookie_str}
        self.http_pool = urllib3.connection_from_url("http://weibo.cn", timeout=5, headers=self.headers)

    def urlopen(self, url):
        res = self.http_pool.urlopen('GET', url, headers=self.headers)
        return res.data


class Friendship():
    '''根据关系网抓取新用户放入工作队列
    '''
    def __init__(self, uid_queue=None):
        self.uid_queue = UidQueue()
        self.db = getDB()
        self.client = WeiboURL()

    def spider(self):
        while True:
            if not self.uid_queue.empty():
                try:
                    uid = self.uid_queue.get()
                    print 'searching user %s follows...' % uid
                    total_page, people_list = self.travel_follow(uid)
                    if len(people_list):
                        self.db.friendships.save({'_id': uid,
                              'follow_list': people_list,
                              'pages': total_page,
                              'last_modify': int(time.time())
                            })
                    else:
                        print 'no update for %s.' % uid
                except Exception, e:
                    LOGGER.error('User %s Follow Page Error: %s' % (uid, e))
            else:
                print 'uid queue empty'
                time.sleep(2)

    def travel_follow(self, uid):
        url = 'http://weibo.cn/'+uid +'/follow'
        img_pattern = r'http://tp(\d+).sinaimg.cn/(\d+)/(\d+)/(\d+)/(\d+)'
        total_page = 1
        follow_page_soup = BeautifulSoup(self.client.urlopen(url+'?page=1'))
        try:
            total_page = int(follow_page_soup.find('div', {'class':'pa', 'id':'pagelist'}).form.div.\
                             find('input', {'name':'mp'})['value'])
        except Exception, e:
            #no follows or follows = 1 page
            pass
        f = self.db.friendships.find_one({'_id': uid})
        try:
            old_people_list = f['follow_list']
            old_total_page = f['pages']
            print 'updating user %s follows...' % uid
        except:
            old_people_list = None
            old_total_page = 0
        pages = range(1, total_page-old_total_page+1)
        random.shuffle(pages)
        people_list = []
        for current_page in pages:
            follow_list = []
            if current_page > 1:
                follow_page_soup = BeautifulSoup(self.client.urlopen(url+'?page='+str(current_page)),
                                                  parseOnlyThese=SoupStrainer('table'))
            for table in follow_page_soup.findAll('table'):
                img_url = table.tr.td.a.img['src']
                r_img = re.search(img_pattern, img_url)
                try:
                    uid = r_img.group(2)
                    follow_list.append(uid)
                except:
                    continue
            for f_uid in follow_list:
                self.uid_queue.add(f_uid)
            people_list.extend(follow_list)
            if old_people_list:
                people_list.extend(old_people_list)
                people_list = list(set(people_list))
            time.sleep(2)
        return total_page, people_list

def main():
    friendship = Friendship()
    friendship.spider()


if __name__ == '__main__': main()
