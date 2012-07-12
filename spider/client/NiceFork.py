#-*- coding:utf-8 -*-

'''新浪微博爬虫涉及到的相关工具函数
'''

import os
import time
import re
import urllib
import urllib2
import cookielib

from BeautifulSoup import BeautifulSoup
from config import LOGGER

#设置cookies文件，
COOKIES_FILE = 'cookies.txt'

def load_cookies(passport):
    '''模拟浏览器登录微博,获取cookies字符串
    '''
    mobile = passport['username']
    password = passport['password']
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


def unix2localtime(ts):
    '''将unix时间戳转化为本地时间格式:2011-1-1 11:11:11
    '''
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))


def smc2unix(date_str):
    '''将微博上的时间格式转化为unix时间戳
    '''
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


def clean_status(status_text):
    '''清洗微博内容 返回清洗后的文本、文本中包含的#话题#、文本中的[表情]
    '''
    t_url_pattern = r'http://t.cn/\w+'
    tag_pattern = r'#(.+?)#'
    emotion_pattern = r'\[(.+?)\]'
    content = re.sub(t_url_pattern, ' ', status_text)
    content = re.sub(tag_pattern, r'\1', content)
    content = re.sub(emotion_pattern, r'', content)
    #print content
    urls = None
    mentions = None
    tags = None
    emotions = None
    rurls = re.findall(t_url_pattern, status_text)
    if rurls:
        urls = []
        for url in rurls:
            urls.append(url)
    rtags = re.findall(tag_pattern, status_text)
    if rtags:
        tags = []
        for tag in rtags:
            #print tag
            tags.append(tag)
    remotions = re.findall(emotion_pattern, status_text)
    if remotions:
        emotions = []
        for emotion in remotions:
            #print emotion
            emotions.append(emotion)
    if tags:
        tags = list(set(tags))
    content = clean_non_alphanumerics(content)
    return content, urls, tags, emotions


def clean_non_alphanumerics(content):
    '''清除文本中除了中文、字母、数字和空格外的其他字符
    '''
    char_list = []
    for char in content:
        n = ord(char)
        if 0x4e00<=n<0x9fa6 or 97<=n<=122 or 65<=n<=90 or 48<=n<=57:
            char_list.append(char)
    return ''.join(char_list)
    
def clean_html(html):
    '''清除html文本中的相关转义符号
    '''
    html = re.sub('&nbsp;', '', html)
    html = re.sub('&ensp;', '', html)
    html = re.sub('&emsp;', '', html)
    html = re.sub('&amp;', '&', html)
    html = re.sub('&lt;', '<', html)
    html = re.sub('&gt;', '>', html)
    html = re.sub('&quot;', '"', html)
    return html

def main():
    content, urls, tags, emotions = clean_status(u'’http://t.cn/123456 @白之兔 //@小白 //@新浪 华人民共和国【】_——『』123中asc文,.<>，。《》 #明天# #今天# 明天得换个笑眯眯的头像。http://t.cn/hqi7Om要不这日子跟着头像走可不得了喽～～～[开心][开心][开心][微笑][大笑][可爱][眨眼][傻笑][坏笑][闭眼][鬼脸二][亲亲]')
    print content
    for url in urls:
        print url
    for tag in tags:
        print tag
    for emotion in emotions:
        print emotion
    
if __name__ == '__main__':
    main()
