#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
import os
import time
import subprocess
import cPickle
import random
import pymongo

from liblinearutil import *
from gensim import corpora, models


class EmotionClassifier(object):

    def __init__(self, dict_name='tweets.dict', model_name='emotion_model'):
        os.chdir('/opt/WeMining/mining/')
        self.dict_name = dict_name
        self.model_name = model_name
        f = open(dict_name, 'rb')
        self.dictionary = cPickle.load(f)
        f.close()

    def cmd_predict(self, texts):
        if not os.path.exists('./tmp/input/'):
            os.makedirs('./tmp/input/')
        if not os.path.exists('./tmp/output/'):
            os.makedirs('./tmp/output/')
        dictionary = self.dictionary
        corpus = [dictionary.doc2bow(text) for text in texts]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        corpus_tfidf = list(corpus_tfidf)
        rows = len(texts)
        current_tmp_ids = [x[:-4] for x in os.listdir('./tmp') if x.endswith('.tmp')]
        new_id = random.randint(0, 65536)
        while str(new_id) in current_tmp_ids :
            new_id = random.randint(0, 65536)
        tfidfFile = open('./tmp/input/%s.tmp' % new_id, 'w')
        results = [0] * rows
        for tnum in range(len(texts)):
            header = '0 '
            tc = header
            for i in corpus_tfidf[tnum]:
                tc += '%s:%s ' % (i[0]+1, i[1])           
            if tc != header:
                results[tnum] = 1
                tfidfFile.write('%s\n' % tc)
        tfidfFile.close()
        cmd = 'liblinear/predict %s %s %s' % ('./tmp/input/%s.tmp' % new_id, self.model_name, './tmp/output/%s.tmp' % new_id)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = None
        while not out:
            out = p.stdout.read()
            time.sleep(1)
        labels_file = open('./tmp/output/%s.tmp' % new_id, 'r')
        lines = labels_file.readlines()
        lines.reverse()
        labels = map(int, lines)
        labels_file.close()
        for index, label in enumerate(results):
            if label:
                results[index] = labels.pop()
        os.remove('./tmp/input/%s.tmp' % new_id)
        os.remove('./tmp/output/%s.tmp' % new_id)
        assert len(labels) == 0
        return results

    def predict(self, texts):
        dictionary = self.dictionary 
        corpus = [dictionary.doc2bow(text) for text in texts]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = list(tfidf[corpus])
        rows = len(texts)
        y = []
        x = []
        model = load_model(self.model_name)
        classes = model.get_labels()
        results = [0] * rows
        for tnum in range(rows):
            features = {}
            for i in corpus_tfidf[tnum]:
                features[i[0]+1] = i[1]
            if len(features.keys()):
                results[tnum] = 1
                y.append(0)
                x.append(features)
        p_labels, p_acc, p_vals = predict(y, x, model)
        labels = [classes[p_val.index(max(p_val))] for p_val in p_vals]
        labels.reverse()
        for index, label in enumerate(results):
            if label:
                results[index] = labels.pop()
        assert len(labels) == 0
        return results
      
    def train(self, step=1, name=1, stage='train'):
        connection = pymongo.Connection()
        db = connection.admin
        db.authenticate('root','root')
        db = connection.emoticon
        text_emotion = []
        for i in range(1, 4):
            for tweet in db['%s_sina_tweets' % i].find(timeout=False):
                text_emotion.append((tweet['key_words'], tweet['eclass']))
        print '%s tweets for training...' % len(text_emotion)
        random.shuffle(text_emotion)
        texts = [t_e[0] for t_e in text_emotion]
        eList = [t_e[1] for t_e in text_emotion]
        f = open(self.dict_name, 'wb')
        dictionary = corpora.Dictionary(texts)
        cPickle.dump(dictionary, f)
        f.close()
        print 'dictionary tweets.dict saved.'
        corpus = [dictionary.doc2bow(text) for text in texts]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf=list(tfidf[corpus])
        y = []
        x = []
        for tnum in range(len(texts)):
            features = {}
            for i in corpus_tfidf[tnum]:
                features[i[0]+1] = i[1]
            if len(features.keys()):
                y.append(int(eList[tnum]))
                x.append(features)
        m = train(y, x, '-s 1')
        save_model(self.model_name, m)
        print 'emotion model saved.'  


def main():
    args = sys.argv
    ec = EmotionClassifier()
    if len(args) > 1:
        task = args[1]
        if task == 'train':
            ec.train()
        elif task == 'test':
            import urllib
            import json
            res = urllib.urlopen('http://idec.buaa.edu.cn/api/public/search.json?q=%E5%A4%8F%E5%A4%A9')
            data = res.read()
            texts = []
            results = json.loads(data)['results']
            for status in results:
                texts.append(status['_keywords'])
            print ec.predict(texts)
        else:
            print 'train for training model.\ntest for test.'


if __name__ == '__main__': main()
