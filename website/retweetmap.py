#-*- coding:utf-8 -*-

import web
import re
import time
import math
import json
import StringIO
import subprocess
import operator

import sys
sys.path.append('..')

import networkx as nx

from tokenizer.fenci import cut
from weibo_search import WeiboSearch
from config import getUser

urls = ('/retweetmap/', '/retweetmap')

render = web.template.render('./templates/', base='layout')

def date2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

def unix2local(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

class handler():
    def GET(self):
        uid = web.cookies().get('WEIBO_UID')
        screen_name, profile_image_url, access_token = getUser(uid)
        form = web.input(q=None, start=None, end=None, count=None)
        q = form.q
        count = form.count
        if not count or count < 0:
            count = 2000
        start = form.start
        end = form.end
        now_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if start and end:
            try:
                start_ts = str(date2ts(start))
                end_ts = str(date2ts(end))
            except:
                return '错误的日期格式,正确格式(YYYY-MM-DD, %s)' % now_day
        else:
            start = '2010-1-1'
            end = now_day
            start_ts = str(date2ts(start))
            end_ts = str(date2ts(end))
        if not q :
           return render.retweetmap_demo(screen_name, profile_image_url, start, end)
        search = WeiboSearch()
        results = search.query(keywords=cut(q, f=['n', 'nr', 'ns', 'nt']), begin=start_ts, end=end_ts, limit=int(count))
        if not results:
            return '没有搜索结果'
        node_ids, node_infos, dot_str, degree_nodes, key_nodes, between_nodes = graph_data(results)
        print 'data ok.'
        svg_str = svg_output(node_ids, node_infos, degree_nodes, key_nodes, between_nodes, dot_str)
        print 'draw ok'
        pagerank_str = '''<div class="section">
	                    <h2>排名最高的人(PageRank)</h2>
	                    <ol>'''
        for key_node in key_nodes:
            li_str = '''<li>
                          <span onclick="snapToUser($('%s'))" onmouseover="mouseOver($('%s'))" onmouseout="mouseOut($('%s'))">%s</span>
                          <br /><br />
                        </li>''' % (node_ids[key_node], node_ids[key_node], node_ids[key_node], key_node)
            pagerank_str += li_str
        pagerank_str += '''</ol>
                       </div>'''

        if not len(between_nodes):
            between_str = '''<div class="section"><h2>排名最高的的人(节点介数)</h2><p>节点数目过多，难于快速计算.</p></div>'''
        else:
            between_str = '''<div class="section">
                                 <h2>排名最高的的人(节点介数)</h2>
                                 <ol>'''
            for between_node in between_nodes:
                li_str = '''<li>
                          <span onclick="snapToUser($('%s'))" onmouseover="mouseOver($('%s'))" onmouseout="mouseOut($('%s'))">%s</span>
                          <br /><br />
                        </li>''' % (node_ids[between_node], node_ids[between_node], node_ids[between_node], between_node)
                between_str += li_str
            between_str += '''</ol>
                      </div>'''

        degree_str = '''<div class="section">
                          <h2>连接数最多的人</h2>
                          <ol>'''
        for degree_node, degree in degree_nodes:
            li_str = '''<li>
                          <span onclick="snapToUser($('%s'))" onmouseover="mouseOver($('%s'))" onmouseout="mouseOut($('%s'))">%s</span><br />
                          <span onclick="snapToUser($('%s'))" onmouseover="mouseOver($('%s'))" onmouseout="mouseOut($('%s'))" class="weak">%s 个连接</span>
                        </li>''' % (node_ids[degree_node], node_ids[degree_node], node_ids[degree_node], degree_node, node_ids[degree_node], node_ids[degree_node], node_ids[degree_node], degree)
            degree_str += li_str

        degree_str += '''</ol>
                     </div>'''

        return render.retweetmap(screen_name, profile_image_url, q, svg_str, pagerank_str, between_str, degree_str, start, end)

def graph_data(results):
    node_ids = {}
    node_infos = {}
    node_index = 0
    g = nx.DiGraph()
    for result in results:
        ts = result['timestamp']
        keywords = result['keywords']
        text = ''.join(keywords).encode('utf-8')
        username = result['username']
        if username not in node_ids:
            node_infos[node_index] = '%s|%s' % (text, ts)
            node_ids[username] = node_index
            node_index += 1
        repost_chain = result['repost_chain']
        if not len(repost_chain):
            if username not in g.nodes():
                g.add_node(username)
            continue
        for from_name in repost_chain:
            from_name = from_name.encode('utf-8')
            if from_name not in node_ids:
                node_ids[from_name] = node_index
                node_index += 1
            g.add_edge(username, from_name)
    degrees = nx.degree(g)
    zero_degree_nodes = [node for node in degrees if degrees[node] == 0]
    dot = ['"%s" -- "%s"' % (n1, n2) for n1, n2 in g.edges()]
    dot.extend(['"%s"' % n for n in zero_degree_nodes])
    dot_str = 'strict graph retweet_networks {\ngraph [layout=sfdp, outputorder=edgesfirst, overlap=prism];\nnode [shape=doublecircle, fixedsize=true, label="", tooltip=""];\nedge [color=grey, label="", tooltip=""];\n%s\n}' % ';\n'.join(dot)
    page_rank = nx.pagerank(g)
    dd = sorted(page_rank.iteritems(), key=operator.itemgetter(1), reverse=True)
    count = 0
    key_nodes = []
    for key, value in dd:
        if count >= 5:
            break
        key_nodes.append(key)
        count += 1
    node_degree = nx.degree(g)
    dd = sorted(node_degree.iteritems(), key=operator.itemgetter(1), reverse=True)
    count = 0
    degree_nodes = []
    for key, value in dd:
        if count >= 5:
            break
        degree_nodes.append((key, value))
        count += 1

    if len(g.nodes()) < 2000:
        betweenness = nx.betweenness_centrality(g)
        dd = sorted(betweenness.iteritems(), key=operator.itemgetter(1), reverse=True)
        count = 0
        between_nodes = []
        for key, value in dd:
            if count >= 5:
                break
            between_nodes.append(key)
            count += 1
    else:
        between_nodes = []
                
    return node_ids, node_infos, dot_str, degree_nodes, key_nodes, between_nodes


def svg_output(node_ids, node_infos, degree_nodes, key_nodes, between_nodes, dot_str):
    degree_nodes = [n[0] for n in degree_nodes]
    graphviz_cmd = subprocess.Popen("sfdp -Tsvg", 
                           stdin=subprocess.PIPE, 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE, 
                           shell = True)
    data_str = graphviz_cmd.communicate(dot_str)[0]
    print 'graphviz scale ok'
    data = StringIO.StringIO(data_str).readlines()
    width = float(re.search(r'width="(\d+)pt"', data[6]).group(1))
    height = float(re.search(r'height="(\d+)pt"', data[6]).group(1))
    size = width if width > height else height
    ratio = 2*size/0.75/96000
    data = data[7:]
    x = 960
    y = 500
    data[0] = '<svg width="100%" height="100%" id="svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" >\n'
    #rename graph
    data[1] = re.sub(r'id="graph1"', 'id="viewport"', data[1])
    data[1] = re.sub(r'transform="scale\(1 1\)', 'transform="scale(%s %s) ', data[1]) % (0.3, 0.3)
    #hack the scale
    data[1] = re.sub(r'translate\(.+\)', ' translate(%s %s)', data[1]) % (1.7*x-width/2, height+y*1.7-height/2)
    #remove polygon
    data.remove(data[2])
    #remove title
    data.remove(data[2])
    comment_pattern = r'<!-- .* -->'
    new_data = []
    node_area = 0
    node_title = None
    inner_circle = 2
    node_lines = []
    for line in data:
        if re.search(r'\r\n', line):
            line = line[:-2]
            line += '\n'
        #remove comments
        if re.search(comment_pattern, line):
            continue
        #remove useless path attr
        line = re.sub(r'<path fill="none" stroke="grey"', '<path', line)
        #changge node attr
        if re.search(r'<g id=.+ class="node"', line):
            node_title = re.search(r'<title>(.*)</title>', line).group(1)
            unichars = re.findall(r'&#(\d+);', node_title)
            if unichars:
                for c in unichars:
                    node_title = re.sub(r'&#%s;' % c, '%s' % unichr(int(c)), node_title.decode('utf-8'))
                    node_title = node_title.encode('utf-8')
            node_area = 1
        else:
            #remove edge title
            line = re.sub(r'<title>(.*)</title>', '', line)
            if node_area:
                if re.search(r'</g>', line):
                    node_area = 0
                    inner_circle = 2
                    new_data.append('<g><text class="user_name">%s</text>\n' % node_title)
                    try:
                        node_name = node_title
                        if node_name in degree_nodes or node_name in key_nodes or node_name in between_nodes:
                            new_data.append('<text class="key">%s</text>\n' % node_infos[node_ids[node_title]])
                        else:
                            new_data.append('<text>%s</text>\n' % node_infos[node_ids[node_title]])
                    except KeyError:
                        new_data.append('<text>%s</text>\n' % '该用户信息不在此数据集中.|该用户信息不在次数据集中.')
                    while len(node_lines):
                        new_data.append(node_lines.pop())
                    node_title = None
                else:
                    if inner_circle:
                        inner_circle = 0
                        line = re.sub(r'<ellipse fill="none" stroke="black"', '<ellipse class="inner" fill="white"', line)
                    else:
                        inner_circle = 1
                        line = re.sub(r'<ellipse fill="none" stroke="black"', '<ellipse id="%s" class="outer" fill="black"' % node_ids[node_title], line)
                    node_lines.append(line)
        if not node_area:
            new_data.append(line)
    return ''.join(new_data)
