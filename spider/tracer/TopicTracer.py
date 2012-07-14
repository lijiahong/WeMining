#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''新浪微博热门话题参与用户跟踪
'''

import os
import time

import math
import md5
import re

import sys
sys.path.append("..")

import urllib
import urllib2
import urllib3
import cookielib

import codecs

from config import load_cookies, smc2unix, unix2localtime
from queues import MidQueue
from BeautifulSoup import BeautifulSoup, SoupStrainer


class WeiboClient(object):
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


class RepostTimeline(object):

    def __init__(self, client, mid, info):
        self.client = client
        self.url = 'http://weibo.cn/repost/'+mid
        self.page_count = 0
        self.mid = mid
        self.info = info
       
    def spider(self):
        if not self.mid or not self.info:
            return None
        f = codecs.open(r'./topics/%s.txt' % self.mid, 'w', encoding='utf-8')
        first_line = '%s %s\n' % (self.mid, self.info)
        print 'new job start', first_line
        f.write(first_line)
        nextPage = 1
        reposts_soup = BeautifulSoup(self.client.urlopen(self.url+'?page='+str(nextPage)))
        source_user_tag = reposts_soup.find('div', {'id':'M_'}).find('div').find('a')
        source_user = {}
        source_user['name'] = source_user_tag.string
        source_user['url'] = source_user_tag['href']
        #print source_user_tag
        total_page = int(reposts_soup.find('div', {'class':'pa', 'id':'pagelist'}).\
                     find('form').find('div').find('input', {'name':'mp'})['value'])
        while total_page > nextPage:
            try:
                reposts_soup = BeautifulSoup(self.client.urlopen(self.url+'?page='+str(nextPage)))
                temp = int(reposts_soup.find('div', {'class':'pa', 'id':'pagelist'}).\
                            find('form').find('div').find('input', {'name':'mp'})['value'])
                deltaPage = temp - total_page
                total_page = temp
                reposts_list = reposts_soup.findAll('div', {'class':'c'})[3:-1]
                for repost in reposts_list:
                    user = repost.find('a')
                    name = user.string
                    url = user['href']
                    tokens = repost.find('span', {'class': 'ct'}).string.split('&nbsp;')#split source & datetime
                    datetime = tokens[0]
                    ts = int(smc2unix(datetime))
                    format_str = '%s %s %s %s %s %s %s ' % self.getUserCount(url)
                    format_str += '%s\n' % ts
                    print format_str
                    f.write(format_str) 
                self.page_count += 1+deltaPage
                nextPage += 1+deltaPage
            except Exception, e:
                self.page_count += 1+deltaPage
                nextPage += 1+deltaPage
                print e
                continue
            time.sleep(0.5)
        f.close()

    def getUserCount(self, url):
        url = 'http://weibo.cn'+url
        user_home_soup = BeautifulSoup(self.client.urlopen(url))
        user_info_div = user_home_soup.find('div', {'class': 'ut'})
        for user_info_div_a in user_info_div.findAll('a'):
            user_info_div_a_result = re.search(r'/(\d+)/info', user_info_div_a['href'])
            if  user_info_div_a_result:
                uid =  user_info_div_a_result.group(1)
                break
        ctt = user_home_soup.find('span', {'class': 'ctt'})
        info_string = ''
        for u_info in ctt.contents:
            try:
                info_string += u_info.string
            except:
                pass
        name, gender, location = info_string.split('/')
        tip2 = user_home_soup.find('div', {'class':'tip2'})
        weibo_count = 0                        
        followee_count = 0
        follower_count = 0
        for br_tag in tip2.contents:
            info_string = br_tag.string
            if info_string:
                rweibo= re.search(u'微博\[(\d+)\]', info_string)
                if rweibo:
                    weibo_count = rweibo.group(1)
                    continue
                rfollower = re.search(u'关注\[(\d+)\]', info_string)
                if rfollower:
                    follower_count = rfollower.group(1)
                    continue  
                rfollowee= re.search(u'粉丝\[(\d+)\]', info_string)
                if rfollowee:
                    followee_count = rfollowee.group(1)
                    continue
        return uid, name, gender, location, weibo_count, follower_count, followee_count

                          
def main():
    client = WeiboClient()
    if not os.path.exists('./topics'):
        os.mkdir('./topics')
    job_list = MidQueue()
    while True:
        if not job_list.empty():
            mid, info = job_list.pop()
            if not mid or not info:
                continue
            RepostTimeline(client, mid, info).spider()
        else:
            time.sleep(5)
        
if __name__ == '__main__': main()
