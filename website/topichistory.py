#-*- coding:utf-8 -*-

'''话题历史页面'''

import time
import web
import pymongo

from config import getDB, getUser

db = getDB()

render = web.template.render('./templates/', base='layout')

urls = ('/topicweibo/history/', '/topicweibo/history')

class handler():
    def GET(self):
        uid = web.cookies().get('WEIBO_UID')
        screen_name, profile_image_url, access_token, expires_in= getUser(uid)
        topic_count_hour = topichash("hour")
        topic_count_day = topichash("day")
        topic_count_week = topichash("week")
        return render.topichistory(screen_name, profile_image_url, topic_count_hour, topic_count_day, topic_count_week)

def topichash(module, type="count"):
    query_dict = {}
    query_dict['type'] = module
    try:
        jsons = db['topics'].find(query_dict, sort=[('ts', pymongo.ASCENDING)])
        topic_countts = {}
        topic_count = []
        for t in jsons:
            if not topic_countts.has_key(t["topic"]):
                topic_countts[t["topic"]] = [(t["count"],t["ts"])]
            else:
                topic_countts[t["topic"]].append((t["count"],t["ts"]))
        for k in topic_countts.keys():
            topic_count.append([k,len(topic_countts[k])])
        if type == "count":
            return topic_count
        if type == "countts":
            return topic_countts
    except:
        return None

if __name__ == '__main__': topichash("week")
