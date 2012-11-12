# -*- coding: utf-8 -*-

import web
import json
import time
import urllib
import math
import csv

import sys
sys.path.append('..')
from tokenizer.fenci import cut

from weibo_search_xapian import WeiboSearch
from config import getDB
from movingaverage import movingaverage
import numpy as np

render = web.template.render('./templates/')

urls = ('/mapweibo/mapview/', '/mapweibo/mapview')

db = getDB()

location2latlon = {}
for p in db.location.find():
    location2latlon[p['location'].encode('utf-8')] = p['latlon']
locations = location2latlon.keys()

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

def date2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

def unix2local(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

def check_location(locations):
    for location in locations:
        try:
            tokens = location.split(' ')
            if len(tokens) == 1:
                province, district = tokens[0], None
            elif len(tokens) == 2:
                province, district = tokens[0], tokens[1]
                if province == u'其他'.encode('utf-8') or province == u'海外'.encode('utf-8'):
                    return False
            else:
                return False
        except:
            return False
    return True

def getLatLon(location):
    if not db.location.find({'location': location}).count():
        q = (u'中国'.encode('utf-8')+location)
        url = 'http://ditu.google.cn/maps/api/geocode/json?address='+urllib.quote(q)+'&sensor=false'
        try:
            result = urllib.urlopen(url).read()
            jsons = json.loads(result, object_hook=_obj_hook)
            #print jsons
            if jsons.status == 'OK':
                p = jsons.results[0].geometry.location
                latlon = '%s %s' % (p.lat, p.lng)
                print 'new location %s:%s' % (location, latlon)
            else:
                return None
        except Exception, e:
            print '%s: Fetch google map api url error: %s!' % (time.ctime(), e)
            return None
        db.location.save({'location': location, 'latlon': latlon})
        time.sleep(0.5)
    else:
        latlon = db.location.find_one({'location': location})['latlon']
    return latlon


class handler():
    def GET(self):
        return render.mapview()

    def POST(self):
        '''
            topic： the keyword you want to search
            starttime: the start time you choose
            endtime: the end time you choose
            alertcoe: alert number = alertcoe * max number, if the increase number > alert number, then alert.
            section: the number of hours you want to do statistical analysis in with each point in the map
            incremental: if the circle data is incremental with concern about the node that is absent in previous data
        '''
        form = web.input(topic=None, starttime=None, endtime=None, alertcoe=None, section=None, incremental=None)
        topic = form.topic
        start = form.starttime
        end = form.endtime
        alertcoe = form.alertcoe
        section = form.section
        incremental = form.incremental
        if topic and start and end:
            start = int(date2ts(start))
            end = int(date2ts(end))
        elif topic:
            start = 0
            end = int(time.time())   
        else:
            return json.dumps({'error': 'wrong paramater.'})
        if alertcoe:
            if int(alertcoe) < 50:
                alertcoe = 0.50
            if int(alertcoe) >= 100:
                alertcoe = 0.99
            if int(alertcoe) >= 50 and int(alertcoe) < 100:
                alertcoe = int(alertcoe)/100.00
        else:
            alertcoe = 0.9#default is 0.9
        if section:
            section = int(section)
        else:
            section = 24 #default is 1 day
        if incremental:
            if incremental == '1':
                incremental = True
            else:
                incremental = False
        ts_arr, results = raw_data(topic, start, end)
        ts_series, groups = partition_time(ts_arr, results, section)
        draw_circle_data = map_circle_data(groups, incremental)        
        max_repost_num, draw_line_data = map_line_data(groups)
        repost_series, fipost_series, post_series, statistic_data= statistics_data(groups, alertcoe)
        '''the length of results in less than input series
        '''
        #print len(list(movingaverage(repost_series, 5, avoid_fp_drift=False)))
        #print moving_average(repost_series, 5, type='simple')
        #print moving_average(repost_series, 5, type='exponential')
        alert_rsi_repost = relative_strength(repost_series, n=14)
        alert_rsi_fipost = relative_strength(fipost_series, n=14)
        alert_rsi_post = relative_strength(post_series, n=14)
        alert_macd_repost = moving_average_convergence(repost_series)
        alert_macd_fipost = moving_average_convergence(fipost_series)
        alert_macd_post = moving_average_convergence(post_series)
        alerts_results = []
        for index in range(0, len(ts_series)):
            alert_dict = {}
            if index in alert_rsi_post[0].keys():
                alert_dict['post_rsi'] = repr(alert_rsi_post[0][index])
            if index in alert_rsi_fipost[0].keys():
                alert_dict['fipost_rsi'] = repr(alert_rsi_fipost[0][index])
            if index in alert_rsi_repost[0].keys():
                alert_dict['repost_rsi'] = repr(alert_rsi_repost[0][index])
            if index in alert_macd_repost[1].keys():
                alert_dict['repost_macd'] = repr(alert_macd_repost[1][index])
            if index in alert_macd_fipost[1].keys():
                alert_dict['fipost_macd'] = repr(alert_macd_fipost[1][index])
            if index in alert_macd_post[1].keys():
                alert_dict['post_macd'] = repr(alert_macd_post[1][index])
            alerts_results.append(alert_dict)
        
        return json.dumps({'statistics_data': statistic_data, 'ts_series': ts_series, 'line': draw_line_data, 'circle': draw_circle_data,
                           'max_repost_num': max_repost_num, 'alert': alerts_results})

def time_series_analysis(dataseries, circle):
    pass
        
def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()


    a =  np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

def relative_strength(prices, n=14):
    """
    compute the n period relative strength indicator
    http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
    http://www.investopedia.com/terms/r/rsi.asp
    """

    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    rising = {}
    falling = {}

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

        if rsi[i] > 60:
            rising[i] = rsi[i]
        elif rsi[i] < 30:
            falling[i] = rsi[i]
        else:
            continue
    return (rising, falling)
        
    #return rsi

def moving_average_convergence(x, nslow=14, nfast=7, mid=3):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    default: nslow=26, nfast=12, mid=9
    """
    emaslow = moving_average(x, nslow, type='exponential')
    emafast = moving_average(x, nfast, type='exponential')
    diff = emafast - emaslow
    dea = moving_average(diff, mid, type='exponential')
    macd = diff - dea

    rising = {}
    falling = {}
    
    for index in range(0, len(x)):
        if index > 0 and macd[index-1] > 0 and macd[index] < 0:
            falling[index] = macd[index]
        elif index > 0 and macd[index-1] < 0 and macd[index] > 0:
            rising[index] = macd[index]
        else:
            continue
    return (rising, falling)       

def raw_data(topic, starttime, endtime, limit=1000):
    global locations, location2latlon
    search = WeiboSearch()
    matches = search.spread_query(keywords=cut(topic), begin=starttime, end=endtime)
    results = []
    ts_arr = []
    for match in matches:
        ts = match['timestamp']
        repost_location = match['repost_location']
        if repost_location != '' and repost_location:
            t_location = match['location']
            f_location = match['repost_location']
            if t_location == '' or f_location == '':
                continue
            if not check_location([t_location, f_location]):
                continue
            f_province = f_location.split(' ')[0]
            t_province = t_location.split(' ')[0]
            latlng_status = 1
            for location in [f_location, t_location, f_province, t_province]:
                if location not in locations:
                    latlng = getLatLon(location)
                    if not latlng:
                        latlng_status = 0
                        break
                    location2latlon[location] = latlng
                    locations = location2latlon.keys()
            if not latlng_status:
                continue
            results.append({'original': 0,
                            '_id': match['_id'],
                            'release_time': match['timestamp'],
                            'forward_address': f_location,
                            'forward_province': f_province,
                            'forward_latlng': location2latlon[f_location],
                            'forward_province_latlng': location2latlon[f_province],
                            'release_address': t_location,
                            'release_province': t_province,
                            'release_province_latlng': location2latlon[t_province],
                            'release_latlng': location2latlon[t_location]
                            })
        else:
            t_location = match['location']
            if t_location == '' and not t_location:
                continue
            if not check_location([t_location]):
                continue
            t_province = t_location.split(' ')[0]
            latlng_status = 1
            for location in [t_location, t_province]:
                if location not in locations:
                    latlng = getLatLon(location)
                    if not latlng:
                        latlng_status = 0
                        break
                    location2latlon[location] = latlng
                    locations = location2latlon.keys()
            if not latlng_status:
                continue
            results.append({'original': 1,
                            '_id': match['_id'],
                            'release_time': match['timestamp'],
                            'release_address': t_location,
                            'release_latlng': location2latlon[t_location],
                            'release_province': t_province,
                            'release_province_latlng': location2latlon[t_province]
                            })
        ts_arr.append(ts)
    return sorted(list(set(ts_arr))), results

def partition_time(ts_arr, data, hournumber):
    ts_series = []
    ts_start = ts_arr[0]
    ts_end = ts_arr[-1]
    each_step = 60*60*hournumber
    ts_current = ts_start
    data_cursor = -1
    groups = []
    while ts_current <= ts_end:
        s_ts = ts_current
        f_ts = ts_current + each_step
        ts_series.append([s_ts, f_ts])
        group = []
        for d in data[data_cursor+1:]:
            ts = d['release_time']
            group.append(d)
            if ts >= f_ts:
                break
            data_cursor += 1
        if len(group):
            groups.append(group)
        ts_current += each_step
    return ts_series, groups

def partition_count(ts_arr, data, section=25):
    ts_series = []
    each_step = int(math.floor(len(ts_arr)/section))
    index = 0
    index += each_step;
    data_cursor = -1
    groups = []
    while index < len(ts_arr):
        p_index = index - each_step
        s_ts = ts_arr[p_index]
        f_ts = ts_arr[index]
        ts_series.append([s_ts, f_ts])
        group = []
        for d in data[data_cursor+1:]:
            ts = d['release_time']
            group.append(d)
            if ts >= f_ts:
                break
            data_cursor += 1
        groups.append(group)
        index += each_step
    return ts_series, groups

def map_circle_data(groups, incremental):
    draw_circle_data = []
    for index, group in enumerate(groups):
        latlng_count_dict = {}
        for status in group:
            release_latlng = status['release_latlng']
            if release_latlng not in latlng_count_dict:
                repost_num = 0
                fipost_num = 0
                j = index
                while j > 0:
                    previous_data = draw_circle_data[index-1]
                    if release_latlng in previous_data:
                        repost_num = previous_data[release_latlng][0]
                        fipost_num = previous_data[release_latlng][1]
                        break
                    else:
                        j -= 1
                latlng_count_dict[release_latlng] = [repost_num, fipost_num]
            if status['original']:
                latlng_count_dict[release_latlng][1] += 1
            else:
                latlng_count_dict[release_latlng][0] += 1
        if incremental == True:
            if index > 0:
                previous_data = draw_circle_data[index-1]
                for release_latlng in previous_data:
                    try:
                        latlng_count_dict[release_latlng]
                    except KeyError:
                        latlng_count_dict[release_latlng] = previous_data[release_latlng]
                        continue
        draw_circle_data.append(latlng_count_dict)
    return draw_circle_data


  
def map_line_data(groups):
    draw_line_data = []
    max_repost_num = 0
    for index, group in enumerate(groups):
        province_repost_count = {}
        for status in group:
            if not status['original']:
                t_province_latlng = status['release_province_latlng']
                f_province_latlng = status['forward_province_latlng']
                key = '%s-%s' % (t_province_latlng, f_province_latlng)
                if key not in province_repost_count :
                    province_repost_count[key] = {'count': 0, 'rank': 0}
                province_repost_count[key]['count'] += 1
        visited = set()
        new_dict = {}
        for key in province_repost_count:
            r_key = reverse_key(key)
            if r_key in visited or key in visited:
                continue
            if key == r_key:
                continue
            count = province_repost_count[key]['count']
            if r_key in province_repost_count:
                r_count = province_repost_count[r_key]['count']
                if count > r_count:
                    count += r_count
                    new_dict[key] = {'count': count,'rank': 0}
                else:
                    r_count += count
                    new_dict[r_key] = {'count': r_count,'rank': 0}
                max_repost_num = max(max_repost_num, count, r_count)
                visited.add(r_key)
            else:
                new_dict[key] = {'count': count,'rank': 0}
                max_repost_num = max(max_repost_num, count)
            visited.add(key)
        province_repost_count = new_dict
        draw_line_data.append(province_repost_count)
    for province_repost_count in draw_line_data:
        for key in province_repost_count:
            count = province_repost_count[key]['count']
            province_repost_count[key]['rank'] = repost_level(count, max_repost_num)
    return max_repost_num, draw_line_data

def statistics_data(groups, alertcoe):
    statistics_data = []
    fipost_series = []
    repost_series = []
    post_series = []
    history_data = []
    alerts = []
    alert = False
    first = True
    max_phi = 0
    max_delta_repost = 0
    max_delta_fipost = 0
    for index, group in enumerate(groups):
        latlng_count_dict = {}
        for status in group:
            release_latlng = status['release_province_latlng']
            province_name = status['release_province']
            if release_latlng not in latlng_count_dict:
                repost_num = 0
                fipost_num = 0
                latlng_count_dict[release_latlng] = [repost_num, fipost_num, province_name]
            if status['original']:
                latlng_count_dict[release_latlng][1] += 1
            else:
                latlng_count_dict[release_latlng][0] += 1
        province_count_repost_dict = {}
        province_count_fipost_dict = {}
        province_count_post_dict = {}
##        province_alert = {}
        all_fipost = 0
        all_repost = 0
        all_post = 0
        for latlng in latlng_count_dict:
            cur_repost = latlng_count_dict[latlng][0]
            cur_fipost = latlng_count_dict[latlng][1]
            all_fipost += cur_repost
            all_repost += cur_fipost
            all_post += all_fipost + all_repost
            province_name = latlng_count_dict[latlng][2]
            pre_repost = 0
            pre_fipost = 0
            j = index
            while j > 0:
                pre_data = history_data[index-1]
                if latlng in pre_data:
                    pre_repost = pre_data[latlng][0]
                    pre_fipost = pre_data[latlng][1]
                    break
                else:
                    j -= 1
            status_repost = -1
            status_fipost = -1
            status_post = -1
            if pre_repost != 0:
                delta_repost = repr(int((cur_repost - pre_repost)*10000/pre_repost)/100.0) + '%'
                if cur_repost - pre_repost > 0:
                    delta_repost = '+' + delta_repost
                    status_repost = 1
            else:
                delta_repost = repr(cur_repost - pre_repost)
                if cur_repost - pre_repost > 0:
                    delta_repost = '+' + delta_repost
                    status_repost = 1
            if pre_fipost != 0:
                delta_fipost = repr(int((cur_fipost - pre_fipost)*10000/pre_fipost)/100.0) + '%'
                if cur_fipost - pre_fipost > 0:
                    delta_fipost = '+' + delta_fipost
                    status_fipost = 1
            else:
                delta_fipost = repr(cur_fipost - pre_fipost)
                if cur_fipost - pre_fipost > 0:
                    delta_fipost = '+' + delta_fipost
                    status_fipost = 1
            if pre_repost + pre_fipost != 0:
                phi = repr(int((cur_repost - pre_repost + cur_fipost - pre_fipost)*10000/(pre_repost + pre_fipost))/100.0) + '%'
                if cur_repost - pre_repost + cur_fipost - pre_fipost > 0:
                    phi = '+' + phi
                    status_post = 1
            else:
                phi = repr(cur_repost - pre_repost + cur_fipost - pre_fipost)
                if cur_repost - pre_repost + cur_fipost - pre_fipost > 0:
                    status_post = 1
            total_post = cur_repost + cur_fipost
            
##            if j > 0:
##                if max_phi < phi:
##                    max_phi = phi
##                if max_delta_repost < delta_repost:
##                    max_delta_repost = delta_repost
##                if max_delta_fipost < delta_fipost:
##                    max_delta_fipost = delta_fipost
                
##            if phi > 200 and first:
##                alert = True
##                province_alert[latlng] = {'name': province_name, 'count': phi}
##            province_alert[latlng] = {'name': province_name, 'count': (phi, delta_repost, delta_fipost)}
                
##            data = [cur_repost, cur_fipost, total_post]
            province_count_repost_dict[province_name] = [cur_repost, delta_repost, repr(status_repost)]
            province_count_fipost_dict[province_name] = [cur_fipost, delta_fipost, repr(status_fipost)]
            province_count_post_dict[province_name] = [total_post, phi, repr(status_post)]
##        if alert:
##            first = False
##        alerts.append(province_alert)
        history_data.append(latlng_count_dict)
        province_count_repost_dict = sorted(province_count_repost_dict.iteritems(), key=lambda(k, v): v[0], reverse=True)
        province_count_fipost_dict = sorted(province_count_fipost_dict.iteritems(), key=lambda(k, v): v[0], reverse=True)
        province_count_post_dict = sorted(province_count_post_dict.iteritems(), key=lambda(k, v): v[0], reverse=True)
        
        statistics_data.append([province_count_repost_dict, province_count_fipost_dict, province_count_post_dict])
        
        repost_series.append(all_repost)
        fipost_series.append(all_fipost)
        post_series.append(all_post)
    return repost_series, fipost_series, post_series, statistics_data                 
##    alerts.append({})
##    alert_phi, alert_delta_repost, alert_delta_fipost = alert_degree(max_phi, max_delta_repost, max_delta_fipost, alertcoe)
##    
##    alerts_results = []
##    count = 0
##    for ale in alerts:
##        if count == 0:
##            alerts_results.append({})
##            count +=1
##            continue
##        count += 1
##        alert_dict = {}
##        for key in ale.keys():
##            latlng = key
##            name = ale[key]['name']
##            phi, delta_repost, delta_fipost = ale[key]['count']
##            status_dict = {}
##            if phi > alert_phi:
##                status_dict['total'] = int(phi*100/max_phi)/100.0
##            else:
##                status_dict['total'] = 0
##            if delta_repost > alert_delta_repost:
##                status_dict['repost'] = int(delta_repost*100/max_delta_repost)/100.0
##            else:
##                status_dict['repost'] = 0
##            if delta_fipost > alert_delta_fipost:
##                status_dict['fipost'] = int(delta_fipost*100/max_delta_fipost)/100.0
##            else:
##                status_dict['fipost'] = 0
##            if status_dict['total'] != 0 or status_dict['repost'] != 0 or status_dict['fipost'] != 0:
##                alert_dict[latlng] = {'name': name, 'status': status_dict}
##        alerts_results.append(alert_dict)
    

def alert_degree(max_phi, max_delta_repost, max_delta_fipost, alertcoe):
    return (round(max_phi*alertcoe), round(max_delta_repost*alertcoe), round(max_delta_fipost*alertcoe))



def repost_level(count, max_repost_num):
    step = int(max_repost_num/3)
    if not count or count <= 0:
        rank = 1
    elif 0 < count <= step:
        rank = 1
    elif step < count <= 2*step:
        rank = 2
    else:
        rank = 3
    return rank
    
def reverse_key(key):
    t_province_latlng, f_province_latlng = key.split('-')
    return '%s-%s' % (f_province_latlng, t_province_latlng)

def main():
    topic = u'钓鱼岛'
    print date2ts('2012-1-1'),date2ts('2012-12-30')
    ts_arr, results = raw_data(topic, int(date2ts('2012-9-1')), int(date2ts('2012-9-20')))
    ts_series, groups = partition_count(ts_arr, results)
    draw_circle_data = map_circle_data(groups)
    max_repost_num, draw_line_data = map_line_data(groups)
    statistic_data, alerts = statistics_data(groups)
    #print alerts
    #return json.dumps({'line': draw_line_data, 'circle': draw_circle_data})

if __name__ == '__main__': main()
        
            
