# -*- coding: UTF-8 -*-

'''根据model.py提取的数据库中的有关话题的微博数据，对其进行预处理，
   为前端程序提供可直接利用的数据
'''
import pymongo
from pymongo import Connection
import json
import model
import time
import urllib

DB_USER_NAME = 'root'
DB_USER_PWD = 'root'
connection = pymongo.Connection()#"219.224.135.60",27017) 
db = connection.admin
db.authenticate(DB_USER_NAME, DB_USER_PWD)
db = connection.weibo

provinceToLatlng = {}
for p in db.province.find():
    provinceToLatlng[p['province'].encode('utf-8')] = p['latlng']
provinces = provinceToLatlng.keys()


def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o

class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

'''检查元素属性release_latlng、forward_province
       是否为null或release_address、forward_address是否为'None'
'''
def latlngAddressIsNotNullOrNone(element):
    status = 'false'
    ori = element['original']
    re_latlng = element['release_latlng']
    re_add = element['release_address']
    if ori == 0:
        fo_latlng = element['forward_latlng']
        fo_add = element['forward_address']
        if re_latlng == 'null' or fo_latlng == 'null' or re_add == 'None' or fo_add == 'None':
            status = 'true'
    if ori == 1:
        if re_latlng == 'null' or re_add == 'None':
            status = 'true'
    return status == 'false'

'''获得元素所在的省份属性
'''
def getProvince(element):
    try:
        ori = element['original']
        if ori == 0:
            re_add = element['release_address']
            fo_add = element['forward_address']
            re_tokens = re_add.split(' ')
            fo_tokens = fo_add.split(' ')
            return (re_tokens[0],fo_tokens[0])
        else:
            r_add = element['release_address']
            r_tokens = r_add.split(' ')
            return r_tokens[0]
    except Exception, e:
        print e
        return 'null'

'''判断元素的两个province属性是否是‘海外’或’其他‘
'''
def addressNotInForeignOrOther(element):
    status = 'false'
    ori = element['original']
    
    province = element['release_province']
    if province == u'海外'.encode('utf-8') or province == u'其他'.encode('utf-8'):
        status = 'true'
    if ori == 0:
        province = element['forward_province']
        if province == u'海外'.encode('utf-8') or province == u'其他'.encode('utf-8'):
            status = 'true'
    return status == 'false'

'''得到中国各省的经纬度坐标
'''
def getProvinceLatlng(province):
    if not db.province.find({'province': province}).count():
        print u'中国'.encode('utf-8') + province + ' latlng is not found in the database'
        q = (u'中国'.encode('utf-8') + province).encode('utf-8')
        url = 'http://ditu.google.cn/maps/api/geocode/json?address='+urllib.quote(q)+'&sensor=false'
        try:
            result = urllib.urlopen(url).read()
            jsons = json.loads(result, object_hook=_obj_hook)
            #print jsons
            if jsons.status == 'OK':
                p = jsons.results[0].geometry.location
                latlng = '%s %s' % (p.lat, p.lng)
                print latlng
            else:
                return 'null'
        except Exception, e:
            print '%s: Fetch google map api url error: %s!' % (time.ctime(), e)
            return None
        db.province.save({'province': province, 'latlng': latlng})
        print u'中国'.encode('utf-8') + province + ' latlng has been written into the database'
        time.sleep(0.5)
    else:
        latlng = db.province.find_one({'province': province})['latlng']
    return latlng

def getUnique(array):
    arr = []
    for i in array:
        if not i in arr:
            arr.append(i)
    return arr

def getData(results):
    '''去掉数组中所有release_latlng、forward_province
       为null或release_address、forward_address为'None'的元素，并检查
    '''
    global provinces, provinceToLatlng
    data = []
    print 'result0.length' + repr(len(results))
    results = filter(latlngAddressIsNotNullOrNone,results)
    print 'result1.length' + repr(len(results))  
    for result in results:
        if not latlngAddressIsNotNullOrNone(result):
            print u'latlng存在null，address存在none'

    '''在results数组元素中加入province和province_latlng属性，形成数组data
    '''
    for result in results:
        if result['original'] == 0:
            re,fo = getProvince(result)
            data.append({'original': result['original'],
                         'release_time': result['release_time'],
                         'forward_address': result['forward_address'],
                         'forward_latlng': result['forward_latlng'],
                         'release_address': result['release_address'],
                         'release_latlng': result['release_latlng'],
                         'release_province': re,
                         'release_province_latlng': '',
                         'forward_province': fo,
                         'forward_province_latlng': ''
                         })
        else:
            data.append({'original': result['original'],
                         'release_time': result['release_time'],
                         'release_address': result['release_address'],
                         'release_latlng': result['release_latlng'],
                         'release_province': getProvince(result),
                         'release_province_latlng': ''
                         })
            
    '''删除数组中所有release_province、forward_province
           是“海外”“海外，其他”“其他”字样的元素
    '''
    data = filter(addressNotInForeignOrOther,data)
    print 'data.length' + repr(len(data))
    for da in data:
        if not addressNotInForeignOrOther(da):
            print u'存在release_address、forward_address为“海外”"其他"'

    ''' 根据release_province、forward_province
           获得release_province_latlng、forward_province_latlng属性
    '''
    for da in data:
        ori = da['original']
        if ori == 0:
            re_province = da['release_province']
            fo_province = da['forward_province']
            if not re_province or not fo_province:
                continue
            if re_province not in provinces:
                provinceToLatlng[re_province] = getProvinceLatlng(re_province)
                provinces = provinceToLatlng.keys()
            if fo_province not in provinces:
                provinceToLatlng[fo_province] = getProvinceLatlng(fo_province)
                provinces = provinceToLatlng.keys()
            da['release_province_latlng'] = provinceToLatlng[re_province]
            da['forward_province_latlng'] = provinceToLatlng[fo_province]       
        else:
            re_province = da['release_province']
            if not re_province:
                continue
            if re_province not in provinces:
                provinceToLatlng[re_province] = getProvinceLatlng(re_province)
                provinces = provinceToLatlng.keys()
            da['release_province_latlng'] = provinceToLatlng[re_province]
    return json.dumps(data)

##def handle(data):
##    raw_data = getData(data)
##    '''对data数组进行再处理，得到画圆数据和画线数据
##    '''
##    time_arr = []
##    for da in raw_data:
##        time_arr.append(da['release_time'])
##    distinct_time_arr = getUnique(time_arr)

    
    
    
if __name__ == '__main__':
    #handle(model.getTopics(u'雷锋'))
    getData(model.getTopics(u'雷锋'))
    
