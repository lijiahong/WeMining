#-*- coding:utf-8 -*-

'''爬虫控制器相关的配置信息
'''

import logging
import sys

#中央控制器地址和端口
HOST = '0.0.0.0'
PORT = 9001

#数据库地址和端口
DB_HOST = 'localhost'
DB_PORT = 27017

#数据库账号信息
DB_USER = 'root'
DB_PWD = 'root'

#登录账号信息
WEIBO_USER = 'linhao1992@gmail.com'
WEIBO_PWD = 'weibomap'

#cookies文件
COOKIES_FILE = 'cookies.txt'

#设置日志记录对象
LOG_FILE = 'log.txt'
LOG_FORMAT = '%(levelname)s %(asctime)-15s %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOGGER = logging.getLogger()
fmt = logging.Formatter(LOG_FORMAT , DATE_FORMAT)
hdlr = logging.FileHandler(LOG_FILE, 'a')
hdlr.setFormatter(fmt)
LOGGER.addHandler(hdlr)
LOGGER.setLevel(logging.INFO)
print >> sys.stderr,'logging ok.'


def getDB():
    '''获取数据库对象
    '''
    connection = pymongo.Connection(DB_HOST, DB_PORT)
    db = connection.admin
    db.authenticate(DB_USER, DB_PWD)
    return connection.weibo


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
