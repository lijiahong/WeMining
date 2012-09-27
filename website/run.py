#-*- coding:utf-8 -*-
#!/usr/bin/env python

import os
import sys
import platform
import time
import web

OOPS_PAGE = '/oops.html'

def import_modules(modules):
    urls = []
    g = globals()
    from imp import load_source
    def import_module(name, file):
        m = load_source(name, file)
        g[name] = m
        v = dir(m)
        h, u = 'handler' in v, 'urls' in v
        if h or u:
            if not (h and u):
                raise ImportError('module %s doesn\'t have matched handler and urls' %name)
            urls.extend(reduce(list.__add__, [[x, '%s.handler' % name] for x in m.urls]))     
    for (name, file) in modules:
        if name not in g:
            import_module(name, file)

    return urls

def _access_log(environ=None, status=''):
    if environ is None and web.ctx.has_key('env'):
        environ = web.ctx.env
    if environ:
        environ['wsgi.errors'].flush()
        host = environ.get('HTTP_X_FORWARDED_FOR') or environ.get('REMOTE_ADDR', '')
        x = host.find(',')
        if x > 0:
            host = host[:x]
        log = [environ.get(x, '') for x in ['SERVER_PROTOCOL', 'REQUEST_METHOD', 'PATH_INFO']]
        x = environ.get('python_backend.request_method')
        if x:
            log[2] = x
        log.insert(0, time.strftime('%Y-%m-%d %H:%M:%S'))
        log.insert(1, host)
        log.append('500 status is None' if status is None else status)
        print >> environ['wsgi.errors'], ','.join(log)
    else:
        print >> sys.stderr, 'bad log format'

class access_log(object):
    def __init__(self, app):
        object.__init__(self)
        setattr(self, 'wrapped_app', app)

    def __call__(self, environ, start_response):
        def xstart_response(status, response_headers, exc_info=None):
            self.status, self.response_headers, self.exc_info = status, response_headers, exc_info
            return start_response(status, response_headers, exc_info)
        setattr(self, 'status', None)
        try:
            try:
                response = self.wrapped_app(environ, xstart_response)
                for data in response:
                    yield data
            except GeneratorExit:
                self.status = '404 no data required'
                raise
            except:
                if self.status is None:
                    start_response('307 Temporary Redirect in access_log', [('Content-Type', 'text/html'), ('Location', OOPS_PAGE)])
        finally:
            _access_log(environ, self.status)

#integrate py file in (url, class) map
argv = sys.argv
current_file = os.path.basename(argv[0])
log = False
debug = False
for arg in argv[1:]:
    if arg == '-port':
        port = argv[argv.index('-port')+1]
    if arg == '-log':
        log = True
    if arg == '-debug':
        debug = True

modules = [(x[:-3], os.path.join('.', x)) for x in os.listdir('.') if x.endswith('.py') and x != current_file]

urls = import_modules(modules)
app = web.application(urls, globals(), False)

if log:
    #access log middleware
    func = app.wsgifunc(access_log, )
else:
    func = app.wsgifunc()

web.config.debug = False

whoami = platform.system()

if whoami == 'Windows' or debug:
    sys.argv[1] = '127.0.0.1:%d' % int(port)
    app.run()

elif whoami =='Linux':
    #is fork better than epoll or select?
    from flup.server.fcgi_fork import WSGIServer
    WSGIServer(func, bindAddress=('127.0.0.1', int(port))).run()
else:
    print 'which system do you use?'

