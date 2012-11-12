#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import xapian
import string
import simplejson as json
import re
import time

sys.path.append('..')
from config import getDB
from tokenizer.fenci import cut


def unix2local(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

def date2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

def index():
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s PATH_TO_DATABASE" % sys.argv[0]
        sys.exit(1)
    db = getDB()
    try:
        # Open the database for update, creating a new database if necessary.
        database = xapian.WritableDatabase(sys.argv[1], xapian.DB_CREATE_OR_OPEN)
        print database, 'open database.'
        emotionvi = 0
        keywordsvi = 1
        timestampvi = 2
        loctvi = 3
        reploctvi = 4
        emotiononlyvi = 5
        usernamevi = 6
        hashtagsvi = 7
        uidvi = 8
        repnameslistvi = 9
        widvi = 10

        count = 0
        time_start = '2012-9-1'
        time_end = '2012-10-1'
        start_time = date2ts(time_start)
        end_time = date2ts(time_end)
        for weibo in db.user_statuses.find({'ts': {'$gte': start_time, '$lte': end_time}}):
            #init
            count += 1
            if count % 10000 == 0:
                print '<------------------>'
                print count, 'at', unix2local(time.time())

            indexer = xapian.TermGenerator()
            stemmer = xapian.Stem("english")
            indexer.set_stemmer(stemmer)
            doc = xapian.Document()
            indexer.set_document(doc)

            #-->username
            username = weibo['name']
    #        print 'username', username
            doc.add_value(usernamevi, username)

            #-->uid
            uid = weibo['uid']
            doc.add_value(uidvi, str(uid))

            #-->wid
            wid = weibo['_id']
            doc.add_value(widvi, wid)

            #-->text
            text = weibo['text'].lower()
            try:
                text += ' ' + weibo['repost']['text'].lower()
            except:
                pass

            #repostnameslist
            repnames_arr = []
            for username in re.findall(r'//@(\S+?):', text):
                if username not in repnames_arr:
                    repnames_arr.append(username)
            try:
                repostname = weibo['repost']['username']
                repnames_arr.append(repostname)
            except:
                pass
            repnames = json.dumps(repnames_arr, ensure_ascii = False)
    #        print 'repostnameslist', repnames
            doc.add_value(repnameslistvi, repnames)

            #@user
            usernames = u''
            for username in re.findall(u"@([\u2E80-\u9FFFA-Za-z0-9_-]+) ?", text):
                usernames += (username + u" ")
            text = re.sub(u"@([\u2E80-\u9FFFA-Za-z0-9_-]+) ?"," ",text)
     #       print 'usernames', usernames

            #hashtag
            hashtags_arr = []
            for hashtag in re.findall(r"#(.+?)#", text):
                hashtag = hashtag.encode('utf-8')
                if hashtag not in hashtags_arr:
                    hashtags_arr.append(hashtag)
            hashtags = ' '.join(hashtags_arr)
    #        print 'hashtags', hashtags
            indexer.index_text(hashtags, 1, 'H')

            #emotion
            emotions_arr = []
            for emotion in re.findall(r"\[(\S+?)\]", text):
                if emotion not in emotions_arr:
                    emotions_arr.append(emotion)
            text = re.sub(r"\[\S+?\]", " " ,text)
            emotions = ' '.join(emotions_arr)
            emotions = emotions.encode('utf-8')
    #        print 'emotions', emotions
            doc.add_value(emotionvi, emotions)

            #emotiononly
            if len(emotions_arr) == 1:
     #           print 'emotiononly', 1
                doc.add_value(emotiononlyvi, xapian.sortable_serialise(1))
            else:
     #           print 'emotiononly', 0
                doc.add_value(emotiononlyvi, xapian.sortable_serialise(0))

            #short url
            text = re.sub(r"http://t\.cn/[-\w]+", " ", text)

            #token
            tokens_arr = cut(text, f=['n', 'nr', 'ns', 'nt'])
            tokens = ' '.join(tokens_arr)
    #        print 'tokens', tokens
            indexer.index_text(tokens)

            #hashtags arr
            hashtags_str = json.dumps(hashtags_arr, ensure_ascii = False)
    #        print 'hashtags_str', hashtags_str.encode('utf-8')
            doc.add_value(hashtagsvi, hashtags_str)

            #keywords
            keywords_hash = {}
            for term in indexer.get_document().termlist():
                keyword = term.term.lstrip('IUHEZ')
                if keyword not in keywords_hash:
                    keywords_hash[keyword] = term.wdf
            keywords = json.dumps(keywords_hash, ensure_ascii = False)
    #        print 'keywords', keywords.encode('utf-8')
            doc.add_value(keywordsvi, keywords)

            #-->ts
            timestamp = weibo['ts']
    #        print 'timestamp', timestamp
            doc.add_value(timestampvi, xapian.sortable_serialise(timestamp))

            #-->location
            location = weibo['location']
    #        print 'location', location
            doc.add_value(loctvi, location)

            #-->repost location
            try:
                repost_location = weibo['repost']['location']
            except:
                repost_location = ''
    #        print 'repost_location', repost_location
            doc.add_value(reploctvi, repost_location)

            # Add the document to the database.
            database.add_document(doc)

        database.flush()
    except Exception, e:
        raise
        print >> sys.stderr, "Exception: %s" % e
        sys.exit(1)

if __name__ == '__main__': index()

