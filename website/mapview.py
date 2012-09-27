# -*- coding: utf-8 -*-

import web
import json
import time
import urllib
import math

import sys
sys.path.append('..')
from tokenizer.fenci import cut

from weibo_search_xapian import WeiboSearch
from config import getDB

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
        form = web.input(topic=None, starttime=None, endtime=None)
        topic = form.topic
        start = form.starttime
        end = form.endtime
        if topic and start and end:
            start = int(date2ts(start))
            end = int(date2ts(end))
        elif topic:
            start = 0
            end = int(time.time())   
        else:
            return json.dumps({'error': 'wrong paramater.'})
        ts_arr, results = raw_data(topic, start, end)
        ts_series, groups = partition_time(ts_arr, results)
        draw_circle_data = map_circle_data(groups)
        max_repost_num, draw_line_data = map_line_data(groups)
        statistic_data, alerts = statistics_data(groups)
        return json.dumps({'statistics_data': statistic_data, 'ts_series': ts_series, 'line': draw_line_data, 'circle': draw_circle_data, 'max_repost_num': max_repost_num, 'alert': alerts})


def raw_data(topic, starttime, endtime, limit=1000, section=25):
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

def partition_time(ts_arr, data, section='day'):
    ts_series = []
    ts_start = ts_arr[0]
    ts_end = ts_arr[-1]
    each_step = 24*60*60
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

def map_circle_data(groups):
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

def statistics_data(groups):
    statistics_data = []
    history_data = []
    alerts = []
    alert = False
    first = True
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
        province_count_dict = {}
        province_alert = {}
        for latlng in latlng_count_dict:
            cur_repost = latlng_count_dict[latlng][0]
            cur_fipost = latlng_count_dict[latlng][1]
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
            delta_repost = cur_repost - pre_repost
            delta_fipost = cur_fipost - pre_fipost
            phi = delta_repost + delta_fipost
            if phi > 200 and first:
                alert = True
                province_alert[latlng] = {'name': province_name, 'count': phi}
            data = [cur_repost, cur_fipost, phi]
            province_count_dict[province_name] = data
        if alert:
            first = False
        alerts.append(province_alert)
        history_data.append(latlng_count_dict)
        province_count_dict = sorted(province_count_dict.iteritems(), key=lambda(k, v): math.fabs(v[2]), reverse=True)
        statistics_data.append(province_count_dict)
    alerts.append({})
    return statistics_data, alerts
           

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
    ts_arr, results = raw_data(topic, date2ts('2012-9-1'), date2ts('2012-9-20'))
    ts_series, groups = partition_count(ts_arr, results)
    draw_circle_data = map_circle_data(groups)
    max_repost_num, draw_line_data = map_line_data(groups)
    statistic_data, alerts = statistics_data(groups)
    print alerts
    # return json.dumps({'line': draw_line_data, 'circle': draw_circle_data})

if __name__ == '__main__': main()
        
            
