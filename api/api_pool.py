#-*- coding:utf-8 -*-

import time
import random
from weibo import APIClient, APIError
from config import APP_KEY, APP_SECRET, CALLBACK_URL, ACCOUNTS, getCode

class APIPool(object):
    def __init__(self, accounts=ACCOUNTS, max_accounts=None):
        usernames = []
        passwords = []
        random.shuffle(accounts)
        if max_accounts and max_accounts > 0:
            accounts = accounts[:max_accounts]
        for account in accounts:
            username, password = account.split()
            print '%s:%s is added.' % (username, password)
            usernames.append(username)
            passwords.append(password)
        self.apis = []
        for username, password in zip(usernames, passwords):
            api = API(username, password)
            self.apis.append(api)
            time.sleep(1)

    def __getattr__(self, attr):
        api = random.choice(self.apis)
        try:
            if not api.is_limited():
                return getattr(api.client, attr)
        except APIError, e:
            if e.error_code == '21327':
                print 'api access token refresh...'
                api.oauth()
            else:
                print 'oops'
            return getattr(api.client, attr)

class API(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = APIClient(APP_KEY, APP_SECRET, redirect_uri=CALLBACK_URL)
        self.oauth()

    def oauth(self):
        auth_url = self.client.get_authorize_url()
        print 'auth: %s' % auth_url
        code = getCode(auth_url, self.username, self.password)
        r = self.client.request_access_token(code)
        self.client.set_access_token(r.access_token, r.expires_in)
        
    def is_limited(self):
        res = self.client.account__rate_limit_status()
        remain = res['remaining_user_hits']
        if remain > 0:
            return False
        return True

    def is_expires(self):
        return self.client.is_expires()

def main():
    api = APIPool(max_accounts=2)
    while True:
        try:
            res = api.statuses__public_timeline(count=200)
            if res:
                statuses = res['statuses']
                for status in statuses:
                    print status['text']
        except Exception, e:
            print e
        time.sleep(10)

if __name__ == '__main__': main()
    
