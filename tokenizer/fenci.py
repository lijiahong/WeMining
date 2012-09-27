#-*- coding:utf-8 -*-

import scws
s = scws.Scws()
s.set_charset('utf-8')
s.set_dict('/usr/local/scws/etc/dict.utf8.xdb',scws.XDICT_MEM)
s.add_dict('/usr/local/scws/etc/dict_cht.utf8.xdb',scws.XDICT_MEM)
s.add_dict('/opt/WeMining/tokenizer/userdic.txt',scws.XDICT_TXT)
s.set_rules('/usr/local/scws/etc/rules.utf8.ini')
s.set_ignore(1)
stopwords = set([line.strip('\r\n') for line in file('/opt/WeMining/tokenizer/ext_stopword.dic')])

#分词模块
def cut(text,f=None):
    global s, stopwords
    if f:
        return [token[0].decode('utf-8') for token in s.participle(text.encode('utf-8')) if token[0] not in stopwords and token[1] in f]
    else:
        return [token[0].decode('utf-8') for token in s.participle(text.encode('utf-8')) if token[0] not in stopwords]

def main():
    for t in cut(u'德罗巴：申花应签下兰帕德和特里 来不为退役'):
        print t

if __name__ == '__main__': main()
