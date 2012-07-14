#!/usr/bin/env python
#-*- coding=utf-8 -*-

'''新浪微博API SDK(Liao Xuefeng,askxuefeng@gmail.com)改进
   基于BasicAuth验证,仅限于应用开发者使用
'''

try:
    import json
except ImportError:
    import simplejson as json
import time
import urllib
import urllib2
import logging
import base64

def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o

class APIError(StandardError):
    '''
    raise APIError if got failed json message.
    '''
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)

class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

def _encode_params(app_key, **kw):
    '''
    Encode parameters.
    '''
    args = []
    args.append('%s=%s' % ('source', app_key))
    for k, v in kw.iteritems():
        qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
        args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)

def _encode_multipart(app_key, **kw):
    '''
    Build a multipart/form-data body with generated random boundary.
    '''
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in kw.iteritems():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            # file-like object:
            ext = ''
            filename = getattr(v, 'name', '')
            n = filename.rfind('.')
            if n != (-1):
                ext = filename[n:].lower()
            content = v.read()
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(ext))
            data.append(content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v.encode('utf-8') if isinstance(v, unicode) else v)
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary

_CONTENT_TYPES = { '.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.jpe': 'image/jpeg' }

def _guess_content_type(ext):
    return _CONTENT_TYPES.get(ext, 'application/octet-stream')

_HTTP_GET = 0
_HTTP_POST = 1
_HTTP_UPLOAD = 2

def _http_call(url, method, app_key, authorization, **kw):
    '''
    send an http request and expect to return a json object if no error.
    '''
    params = None
    boundary = None
    if method==_HTTP_UPLOAD:
        params, boundary = _encode_multipart(app_key, **kw)
    else:
        params = _encode_params(app_key, **kw)
    http_url = '%s?%s' % (url, params) if method==_HTTP_GET else url
    http_body = None if method==_HTTP_GET else params
    req = urllib2.Request(http_url, data=http_body)
    if authorization:
        req.add_header("Authorization", "Basic %s" % authorization)
    if boundary:
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    resp = urllib2.urlopen(req)
    body = resp.read()
    r = json.loads(body, object_hook=_obj_hook)
    if hasattr(r, 'error_code'):
        raise APIError(r.error_code, getattr(r, 'error', ''), getattr(r, 'request', ''))
    return r

class HttpObject(object):

    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):
        def wrap(**kw):
            return _http_call('%s%s.json' % (self.client.api_url, attr.replace('__', '/')), self.method, self.client.app_key, self.client._b64up, **kw)
        return wrap

class APIClient(object):
    '''
    API client using synchronized invocation.
    '''
    def __init__(self, username, password, app_key):
        self.app_key = app_key
        self._b64up = base64.b64encode('%s:%s' % (username, password))
        self.api_url = 'http://api.t.sina.com.cn/'
        self.get = HttpObject(self, _HTTP_GET)
        self.post = HttpObject(self, _HTTP_POST)
        self.upload = HttpObject(self, _HTTP_UPLOAD)

    def __getattr__(self, attr):
        return getattr(self.get, attr)

def main():
    api = APIClient('linhao1992@gmail.com', 'weibomap', '2298231745')
    print api.account__rate_limit_status()

if __name__ == '__main__': main()
