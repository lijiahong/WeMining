#-*-coding:utf-8-*-

import web
import re
import time

from weibo import APIClient
from config import getDB
from config import APP_KEY, APP_SECRET, CALLBACK_URL

urls = ('/callback', )

db= getDB()

img_pattern = r'http://tp\d+.sinaimg.cn/\d+/(\d+)/\d+/\d+'

class handler():
    def GET(self):
        try:
            query = web.ctx['query']
            code = re.search(r'\?code=(.+)', query).group(1)
        except:
            return 'need code.'
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        try:
            r = client.request_access_token(code)
            access_token = r.access_token
            expires_in = r.expires_in
            client.set_access_token(access_token, expires_in)
        except:
            return 'login failed.'
        uid = None
        try:
            uid = client.account__get_uid()['uid']
            userinfo = client.get.users__show(uid=uid)
            screen_name = userinfo['screen_name']
            profile_image_url = userinfo['profile_image_url']
            profile_image_url = '/30/'.join(profile_image_url.split('/50/'))
            web.setcookie('WEIBO_UID', uid, expires="", domain='.buaa.edu.cn', secure=False)
            db['weibo_users'].save({'_id': str(uid), 
                                    'access_token': access_token, 
                                    'expires_in': expires_in, 
                                    'screen_name': screen_name, 
                                    'profile_image_url': profile_image_url}, safe=True)
        except Exception, e:
            print '%s %s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), uid, e)
            return 'get user info failed'
        web.redirect('/')
            
        
