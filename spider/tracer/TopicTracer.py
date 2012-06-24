#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''新浪微博热门话题参与用户跟踪
'''

import os
import time

import math
import md5
import re

import urllib
import urllib2
import urllib3
import cookielib

import codecs

from queues import MidQueue
from BeautifulSoup import BeautifulSoup, SoupStrainer


COOKIES_FILE = 'cookies.txt'
WEIBO_USER = 'linhao1992@gmail.com' 
WEIBO_PWD = 'weibomap'


def unix2localtime(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))


def smc2unix(date_str):
    time_pattern_1 = r'(\d+)'+u'分钟前' #5分钟前
    time_pattern_2 = u'今天'+r' (\d\d):(\d\d)' #今天 17:51
    time_pattern_3 = r'(\d\d)'+u'月'+r'(\d\d)'+u'日 '+r'(\d\d):(\d\d)' #02月22日 08:32 
    time_pattern_4 =  r'(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)' #2011-12-31 23:34:19
    date_str.strip()
    try:
        minute = int(re.search(time_pattern_1, date_str).group(1))
        now_ts = time.time()
        ts = now_ts - minute*60
        #print time.localtime(ts)
        return ts
    except:
        pass
    try:
        hour = re.search(time_pattern_2, date_str).group(1)
        minute = re.search(time_pattern_2, date_str).group(2)
        now = time.localtime()
        date = str(now.tm_year)+'-'+str(now.tm_mon)+'-'+str(now.tm_mday)+' '+hour+':'+minute
        ts = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M'))
        #print time.localtime(ts)
        return ts
    except:
        pass
    try:
        month = re.search(time_pattern_3, date_str).group(1)
        day = re.search(time_pattern_3, date_str).group(2)
        hour = re.search(time_pattern_3, date_str).group(3)
        minute = re.search(time_pattern_3, date_str).group(4)
        now = time.localtime()
        date = str(now.tm_year)+'-'+month+'-'+day+' '+hour+':'+minute
        ts = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M'))
        #print time.localtime(ts)
        return ts
    except:
        pass
    try:
        year = re.search(time_pattern_4, date_str).group(1)
        month = re.search(time_pattern_4, date_str).group(2)
        day = re.search(time_pattern_4, date_str).group(3)
        hour = re.search(time_pattern_4, date_str).group(4)
        minute = re.search(time_pattern_4, date_str).group(5)
        second = re.search(time_pattern_4, date_str).group(6)
        date = year+'-'+month+'-'+day+' '+hour+':'+minute+':'+second
        ts = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S'))
        #print time.localtime(ts)
        return ts
    except:
        pass
    return None


def load_cookies():
    '''模拟浏览器登录微博,获取cookies字符串
    '''
    mobile = WEIBO_USER
    password = WEIBO_PWD
    cookie_str = '' 
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
