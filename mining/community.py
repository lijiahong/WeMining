#!/usr/bin/env python
#-*-coding:utf-8-*-

import pymongo
import networkx as nx
import cPickle
import codecs

connection = pymongo.Connection()
db = connection.admin
db.authenticate('root','root')
db = connection.weibo

# G = nx.DiGraph()

# results = db.friendships.find()
# print results.count()
# for friendships in results:
#     fid = int(friendships['_id'])
#     follow_list = friendships['follow_list']
#     for tid in follow_list:
#         tid = int(tid)
#         G.add_edge(fid, tid)

# c = list(nx.k_clique_communities(G, int(1000)))

# f = open(r'c.list', 'wb')
# cPickle.dump(c, f)
# f.close()

uids = set()
users = db.users.find()
for user in users:
    uid = int(user['_id'])
    try:
        pages = user['pages']
    except:
        pages = 0
    if pages:
        uids.add(uid)
results = db.friendships.find()
line_index = 0
f = codecs.open('follow_list.txt', 'w', encoding='utf-8')
for friendships in results:
    fid = int(friendships['_id'])
    follow_list = friendships['follow_list']
    last_modify = friendships['last_modify']
    if fid not in uids:
        continue
    for tid in follow_list:
        tid = int(tid)
        if fid not in uids:
            continue
        f.write('%s %s %s %s\n' % (line_index, fid, tid, last_modify))
        line_index += 1
f.close()

        
        
