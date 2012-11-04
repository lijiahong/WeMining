# -*- coding=utf-8 -*-

import networkx as nx
import pymongo
import operator
import re
import codecs

connection = pymongo.Connection()
db = connection.admin
db.authenticate('root','root')
db = connection.master_timeline

results = db.master_timeline_weibo.find()
g = nx.DiGraph()

status_count = 0
def mid2status(mid):
    return db.master_timeline_weibo.find_one({'_id': mid})

for status in results:
    if status_count%1000 == 0:
        print status_count
    if len(status['reposts']):
        name = status['user']['name']
        repost_list = status['reposts']
        for mid in repost_list:
            status = mid2status(mid)
            text = status['text']
            re_user = re.findall(r'//@(\S+?):', text)
            if re_user and len(re_user):
                r_name = re_user[0]
            else:
                r_name = status['user']['name']
            try:
                c_weight = g[r_name][name]['weight']
                g.add_edge(r_name, name, weight=c_weight+1)
            except:
                g.add_edge(r_name, name, weight=1)
    status_count += 1

f = codecs.open('output.txt', 'w', encoding='utf-8')
page_rank = nx.pagerank(g, weight='weight', max_iter=5000)
dd = sorted(page_rank.iteritems(), key=operator.itemgetter(1), reverse=True)
count = 0
max_count = 100
key_nodes = []
print 'total person: %s' % len(g.nodes())

print 'pagerank'
for key, value in dd:
    if value < 10**-4:
        break
    if count >= max_count:
        break
    f.write('%s %s\n' % (key, value))
    key_nodes.append(key)
    count += 1
f.write('--------------------\n')
print 'degree'
node_degree = nx.degree(g)
dd = sorted(node_degree.iteritems(), key=operator.itemgetter(1), reverse=True)
count = 0
degree_nodes = []
for key, value in dd:
    if count >= max_count:
        break
    f.write('%s %s\n' % (key, value))
    degree_nodes.append(key)
    count += 1
f.close()
