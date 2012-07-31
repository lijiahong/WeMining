#-*- coding:utf-8 -*-

import re
import urllib
import urllib2
import mechanize


APP_KEY = '999494363'
APP_SECRET = '53384a9bd6c88d1fa44f9d5ede95d58b'
CALLBACK_URL = 'http://127.0.0.1:88799/callback'

code = None

class HTTPRedirectHandlerForCode(urllib2.BaseHandler):
    def http_request(self, request):
        global code
        if hasattr(request, "redirect_dict"):
            call_back_url = request.get_full_url()
            try:
                code = re.search(CALLBACK_URL+'\?code=(.+)', call_back_url).group(1)
            except:
                pass
        return request


def getCode(auth_url, username, password):
    '''
       this is NOT thread safe due to the global var code
    '''
    br = mechanize.Browser()
    br.handler_classes['_debug_redirect'] = HTTPRedirectHandlerForCode
    br.set_handle_robots(False)
    br.set_handle_equiv(False)
    br.set_handle_refresh(False)
    br.set_debug_redirects(True)
    br.open(auth_url)
    br.select_form(name='authZForm')
    br['userId'] = username
    br['passwd'] = password
    try:
        response = br.submit()
    except urllib2.URLError:
        #no reponse from callback
        pass
    return code

