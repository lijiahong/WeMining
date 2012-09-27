#-*- coding:utf-8 -*-

import re
import urllib
import urllib2
import mechanize


APP_KEY = '4131380600'
APP_SECRET = 'df544af4a9e30abe16e715cb4d0be423'
CALLBACK_URL = 'http://idec.buaa.edu.cn:8080/callback'
ACCOUNTS = ['hanyangprint@126.com hanyang' ,'hope_thebest@sina.com hanyang' ,'hope_thebest@msn.com hanyang']

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

