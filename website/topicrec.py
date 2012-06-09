# -*- coding: UTF-8 -*-
'''网站接入用户，接受授权，获取用户关注的话题
'''
import os
import sys
import json
import web
import webbrowser
import urllib
from weibo import APIClient

def getTopicByRec(module):
    if module == 'all':
        weighted_output = [u'世界无烟日',9.99,u'舌尖上的中国',8.01,u'环球时报',6,u'学生应该脱鞋自己走',3.99,u'新iphone疑似谍照曝光',2.01,u'裁员',9.99,u'钱夹',8.01,u'十九',6,u'戴尔',3.99,u'翁美玲',2.01]
        return weighted_output
    if module == 'personal':
        weighted_output = [u'雷锋',14,u'朝鲜',18,u'伊朗',16,u'薄熙来',16,
                          u'两会',14,u'云',12,u'名古屋',11, u'甄嬛传', 6]
        return weighted_output

if __name__ == '__main__':
    getTopicByRec()

