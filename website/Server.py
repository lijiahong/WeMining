# -*- coding: utf-8 -*-

'''web服务器
'''

import time
import sys
import web
import model
import prehandle
import topicrec
import app_config
from weibo import APIClient
import webbrowser
import getWeiboNum
#import session
import pymongo
from pymongo import Connection
import json
import math
import time
import datetime

DB_USER_NAME = 'root'
DB_USER_PWD = 'root'
connection = pymongo.Connection()#'219.224.135.60',27017)
db = connection.admin
db.authenticate(DB_USER_NAME, DB_USER_PWD)
db = connection.weibo

#web.config.debug = False #退出调试模式


urls = (
    '/(.*)/', 'Redirect', #保证url有无'/' 结尾，都能指向同一个类
    '/weiming','Weiming',
    '/weiming/about','About',
    '/weiming/spidermonitor','SpiderMonitor',
    '/weiming/mapweibo','MapWeibo',
    '/weiming/mapweibo/mapview','MapView',
    '/pathdata/(.+)','PathData',
    '/gettopics/(.+)', 'Gettopics',
    '/login','Login',
    '/callback','CallBack',
    '/logout','LogOut',
    '/count/.*', 'Count',
    '/data/(.+)', 'Data',
    '/weiming/mapweibo/sentiment','Sentiment',
    '/slider','slider',
    '/errorpage','Error',
    '/getWeiboNum','GetWeiboNum'
)

app = web.application(urls, globals())

#在调试模式下运行session
if web.config.get('_session') is None:
    #web.py中有三种session机制，本应用采用session保存在本地磁盘中的机制
    session = web.session.Session(app, web.session.DiskStore('sessions'),initializer={'access_token': None,'uid':None,'expires_in':None,
                                                                                      'user_screen_name':None,'user_profile_image_url':None,'user_weibo_url':None})
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('templates/')

class GetWeiboNum:
    def GET(self):
        form = web.input(topic=None,filename=None)
        print form.topic
        print form.filename
        return getWeiboNum.getWeiboNum(form.topic,form.filename)
class Redirect:
    def GET(self, path):
        web.seeother('/' + path)
class Weiming:
    def GET(self):
        return render.weiming()
class About:
    def GET(self):
        return render.about()
class SpiderMonitor:
    def GET(self):
        return render.spider()
class MapWeibo:
    def GET(self):
        uid = session.get('uid',None)
        user_screen_name=session.get('user_screen_name',None)
        user_profile_image_url=session.get('user_profile_image_url',None)
        user_weibo_url=session.get('user_weibo_url',None)
        if uid == None or user_screen_name == None or user_profile_image_url == None or user_weibo_url == None:
            return render.mapweibo(uid=None,user_screen_name=None,user_profile_image_url=None,user_weibo_url=None)
        else:
            return render.mapweibo(uid=uid,user_screen_name=user_screen_name,user_profile_image_url=user_profile_image_url,user_weibo_url=user_weibo_url)
        
class MapView:
    def GET(self):
        return render.mapview()
    def POST(self):
        form = web.input(topic=None,starttime=None,endtime=None)
        if form.topic and form.starttime and form.endtime:
            print form.topic#"topic:%s,starttime:%d,endtime:%d"%(form.topic,form.starttime,form.endtime)
            print form.starttime
            print form.endtime
            s1 = form.starttime
            s2 = form.endtime           
            d1 = datetime.datetime.strptime(s1,"%Y/%m/%d")
            d2 = datetime.datetime.strptime(s2,"%Y/%m/%d")

            print time.mktime(d1.timetuple())
            print time.mktime(d2.timetuple())
            d1 = time.mktime(d1.timetuple())
            d2 = time.mktime(d2.timetuple())
            try:
               results = prehandle.getData(model.getTopics(form.topic.encode('utf-8'),math.floor(float(d1)),math.floor(float(d2))))#1331084340.0,1331196940.0))#form.topic,int(form.starttime),int(form.endtime)))
               return results
            except Exception,ex:
               print Exception,":",ex
               web.seeother('/errorpage')
               #return "data error"
        else:
            return "please select proper topic ,starttime and endtime before posting your request again"
        
class Sentiment:
    def GET(self):
        return render.sentimentview()
class slider:
    def GET(self):
        return render.testslider()
class Error:
    def GET(self):
        return render.error()
#首先从session中获取access_token，没有就转向新浪微博页面认证
#认证成功后将access_token保存在session中
class Login:
    def GET(self):
        access_token = session.get('access_token',None)
        uid = session.get('uid',None)
        expires_in = session.get('expires_in',None)
        if access_token != None and uid!=None and expires_in!=None:
            client = APIClient(app_config.APP_KEY, app_secret=app_config.APP_SECRET, redirect_uri=app_config.CALLBACK_URL)
            client.set_access_token(access_token,expires_in)
            return showUserInfo(client,uid,expires_in)
        else:
            client = APIClient(app_key=app_config.APP_KEY, app_secret=app_config.APP_SECRET, redirect_uri=app_config.CALLBACK_URL)
            url = client.get_authorize_url()
            web.seeother(url)
def showUserInfo(client,uid,expires_in):
    user_info = client.get.users__show(uid=uid)
    user_screen_name = user_info['screen_name']
    user_profile_image_url = user_info['profile_image_url']
    user_weibo_url = 'http://weibo.com/u/' + repr(uid)
    session['user_screen_name'] = user_screen_name
    session['user_profile_image_url'] = user_profile_image_url
    session['user_weibo_url'] = user_weibo_url
    web.seeother('/weiming/mapweibo')
    #return render.mapweibo(uid=uid,user_screen_name=user_screen_name,user_profile_image_url=user_profile_image_url,user_weibo_url=user_weibo_url)
    
class CallBack:
    def GET(self):
        #在session中保存code，用于在新浪微博认证通过后换取access_token
        code = web.input(code=None).code       
        client = APIClient(app_config.APP_KEY, app_secret=app_config.APP_SECRET, redirect_uri=app_config.CALLBACK_URL)
        r = client.request_access_token(code)
        access_token = r.access_token # 新浪返回的token
        expires_in = r.expires_in # token过期的UNIX时间
        client.set_access_token(access_token, expires_in)
        user_uid = client.get.account__get_uid()
        # TODO: 在此保存access token等保存到session中
        session.access_token=access_token
        session.expires_in=expires_in
        session.uid = user_uid['uid']
        
        uid = user_uid['uid']
        return showUserInfo(client,uid,expires_in)
class LogOut:
    def GET(self):
        del session['access_token']
        del session['uid']
        del session['expires_in']
        del session['user_screen_name']
        del session['user_profile_image_url']
        del session['user_weibo_url']
        web.seeother('/weiming/mapweibo')
class PathData:
    def GET(self):
        form = web.input(topic=None,starttime=None,endtime=None)
        if form.topic and form.starttime and form.endtime:
            print form.topic#"topic:%s,starttime:%d,endtime:%d"%(form.topic,form.starttime,form.endtime)
            print form.starttime
            print form.endtime
            print form.timeInterval
            try:
               results = prehandle.getData(model.getTopics(form.topic,form.starttime,form.endtime))
               return results
            except Exception,ex:
               print Exception,":",ex
               return "data error"
        else:
            return "please select proper topic ,starttime and endtime before posting your request again"
        

class Topic:        
    def GET(self, topic):
        return prehandle.getData(model.getTopics(topic))

class Count:
    def GET(self):
        return model.getCount()

class Data:
    def GET(self,topic):
        return prehandle.getData(model.getTopics(topic))
class Gettopics:
    def GET(self,module):
        return json.dumps(topicrec.getTopicByRec(module))
        
if __name__ == "__main__":
    app.run()

