#-*- coding:utf-8 -*-

import pymongo
import scws

#数据库地址和端口
DB_HOST = 'localhost'
DB_PORT = 27017

#数据库账号信息
DB_USER = 'root'
DB_PWD = 'root'

def getDB():
    '''获取数据库对象
    '''
    connection = pymongo.Connection(DB_HOST, DB_PORT)
    db = connection.admin
    db.authenticate(DB_USER, DB_PWD)
    return connection.weibo


#分词模块
def cut(text,f=['n', 'nr', 'ns', 'nt'])
    s = scws.Scws()
    s.set_charset('utf-8')
    s.set_dict('/usr/local/scws/etc/dict.utf8.xdb',scws.XDICT_MEM)
    s.add_dict('/usr/local/scws/etc/dict_cht.utf8.xdb',scws.XDICT_MEM)
    s.add_dict('userdic.txt',scws.XDICT_TXT)
    s.set_rules('/usr/local/scws/etc/rules.utf8.ini')
    s.set_ignore(1)
    stopwords = set([line.strip('\r\n') for line in file('ext_stopword.dic')])
    return [token[0] for token in s.participle(text.encode('utf-8')) if token[0] not in stopwords and token[1] not in f]
    
