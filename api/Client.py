#!/usr/bin/env python
#-*-coding=utf-8-*-


import time
import re
import socket
import urllib
import json
import random
import md5

# from api_pool import APIPool

class API(object):
    def __init__(self):
        pass

    def usertimeline(self, uid, page):
        url = 'https://api.weibo.com/2/statuses/user_timeline.json?uid=%s&page=%d&count=100&access_token=2.00TMVxDCyoqaVE9a6853656fxJtgHB' % (uid, page)
        resp = urllib.urlopen(url)
        data = resp.read()
        return json.loads(data)

api = API()

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
source_a_pattern = r'<a(.+?)>(.+?)</a>'

HOST = '219.224.135.60'
PORT = 9001

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


def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X
    
    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num


def id2mid(id_str):
    mid_stack = []
    for i in range(len(id_str)-7, -7, -7):
        offset1 = 0 if i<0 else i
        offset2 = i+7
        num = id_str[offset1:offset2]
        num = base62_encode(int(num))
        mid_stack.append(num)
    mid = ''
    while len(mid_stack):
        mid += mid_stack.pop()
    return mid


def local2unix(time_str):
    time_format = '%a %b %d %H:%M:%S +0800 %Y'
    return time.mktime(time.strptime(time_str, time_format))

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

def spider(uid):
    page = 1
    user_statuses = []
    while page < 3:
        user_statuses.extend(api.usertimeline(uid, page)['statuses'])
        page += 1
    if not user_statuses and not len(user_statuses):
        time.sleep(1)
        return None
    posts = []
    for status in user_statuses:
        mid = id2mid(str(status['id']))
        uid = status['user']['id']
        ts = local2unix(status['created_at'])
        content = None
        urls = None
        hashtags = None
        emotions = None
        source = status['source']
        rsource = re.search(source_a_pattern, source)
        if rsource:
            source = rsource.group(2)
        else:
            continue
        text = status['text']
        name = status['user']['name']
        gender = status['user']['gender']
        location = status['user']['location']
        content, urls, hashtags, emotions = clean_status(text)
        post = {'_id': mid,
                'uid': uid,
                'name': name,
                'gender': gender,
                'location': location,
                'text': text,
                'source': source,
                'ts': ts,
                'urls': urls,
                'hashtags': hashtags,
                'emotions': emotions,
                '_md5': md5.new((str(uid)+text).encode('utf-8')).hexdigest()}
        print post['text']
        try:
            rt = status['retweeted_status']
            if rt:
                re_user = status['retweeted_status']['user']
                source_text = status['retweeted_status']['text']
                repost =  {'uid': re_user['id'],
                           'name': re_user['name'],
                           'gender': re_user['gender'],
                           'location': re_user['location'],
                           'text': source_text,
                           '_md5': md5.new((str(re_user['id'])+source_text).encode('utf-8')).hexdigest()}
                post['repost'] = repost
                print 'repost: %s' % source_text
        except KeyError:
            pass
        posts.append(post)
    return posts

class Spider(object):
    def __init__(self):
        self.socket = socket.socket()

    def postdata(self, **kw):
        try:
            data = kw['data']
        except:
            return None
        self.socket.sendall(json.dumps({'action': 'postdata', 'data': data})+ '\r\n')
        res = recv_line(self.socket)
        r = json.loads(res)
        if 'error' in r:
            LOGGER.error(r['error'])
            return None
        else:
            return r['status']
    
    def getuid(self):
        self.socket.sendall(json.dumps({'action': 'getuid'})+ '\r\n')
        res = recv_line(self.socket)
        r = json.loads(res)
        if 'error' in r:
            LOGGER.error(r['error'])
            return None
        else:
            return r['uid']

    def request(self, action=None, **kw):
        func = getattr(self, action)
        return func(**kw)

    def run(self):
        self.socket.connect((HOST ,PORT))
        while True:
            uid = self.request(action='getuid')
            if uid:
                print 'searching %s...' % uid
                posts = spider(uid)
                if posts and len(posts):
                    status = self.request(action='postdata', data={'user_statuses': posts})
                    print '%s %d statuses: %s' % (uid, len(posts), status)
                else:
                    print '%s no data.' % uid
            else:
                time.sleep(3)
        self.socket.close()

def main():
    s = Spider()
    s.run()

if __name__ == '__main__': main()
