#-*- coding:utf-8 -*-
#!/usr/bin/env python

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

import sys
sys.path.append("..")

from BeautifulSoup import BeautifulSoup, SoupStrainer
from config import LOGGER, load_cookies, getDB
from queues import UidQueue


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
