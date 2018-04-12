#!/usr/bin/env python
#coding: utf-8

'''
@auther: 王坤
create time：2017年4月21日
'''

import os, sys, time, pycurl, codecs, glob, requests

try:
    import urllib,urllib2
except Exception:
    import urllib.request as urllib
    import urllib.request as urllib2
    
import gevent
from gevent import monkey
monkey.patch_socket()
import gevent.pool

from crawler import *
from crawler import content, lang

def file_name(langages, i, filename, lik):
    itmp = i.strip().replace('\n', '').replace('\r', '').split('=')
    if len(itmp) == 3:
        try: 
            links = itmp[2].replace('\n', '')
            if '://' not in links: 
                if '//' == links[:1]:
                    pass
                elif '/' ==links[0]:
                    proto, rest = urllib.splittype(links)
                    rest1, res2 = urllib.splithost(rest)
                    links = 'http://' + rest1 + links if rest1 else links
                else:
                    links = 'http://' + links
            print ('正在检测的url：%s' % links)
            response = None
            try:
                req = urllib2.Request(links,headers={'Referer': links})
                req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
                response = urllib2.urlopen(req, timeout=20)
                txtfile = response.read()
            except urllib2.URLError as e:
                linksobj = requests.get(links,headers={'Referer': links}, timeout=20)
                linkcode = linksobj.status_code
                if 200 == linkcode:
                    txtfile = linksobj.text
                else:
                    txtfile = ''
            if txtfile:
                try:
                    txtfiles = txtfile.decode("utf-8", 'ignore')
                    fin = content.main(txtfiles)
                except Exception:
                    fin = content.main(txtfile)
            
                #以读的方式打开输入文件
                try:
                    res = langages.translate(fin, filename + "myOutputFile.txt", lik, 500)
                except Exception as err:
                    fin = fin.encode('utf-8')
                    res = langages.translate(fin, filename + "myOutputFile.txt", lik, 500)
                if os.path.exists(filename + "myOutputFile.txt"):
                    os.remove(filename + "myOutputFile.txt")
                if res:
                    print ('可用网站的地址：%s' % links)
                    fname =  filename + '-right.conf'
                else:
                    fname =  filename + '-wrong.conf'
            else:
                fname =  filename + '-error.conf'
            with codecs.open(fname, 'a', 'utf-8') as fp:
                fp.writelines([i])
        except Exception as err:
            print (err)
        print ('网站配置%s检测完毕！' % i)
    else:
        print (i)

def curl_webSev():
    filenames = input('查找的文件名称（默认：conf/Russian.conf）:')
    if not filenames: filenames = 'conf/Russian.conf'
    for filename in glob.glob(filenames):
        with codecs.open(filename, 'r', "utf-8") as fp:
            contents = fp.readlines()
        langages = lang.LangagesofFamily()
        print (langages.lanclass)
        print (filename)
        lik = input("请输入一个圆括号的内容，如：\"(['zh'] ,'Chinese_Simp')\" >>>")  
        lik = eval(lik)
        print ('start:%s' % time.ctime())

        # 提高IO并发量
        # jobs = [gevent.spawn(file_name, langages, i, filename, lik) for i in contents]
        # gevent.joinall(jobs)
        # 使用协程池 
        dataList = []
        pool=gevent.pool.Pool(500)
        for i in contents:
            dataList.append(pool.spawn(file_name, langages, i, filename, lik))
        pool.join()
        
        #for i in contents:
        #    file_name(langages, i, filename, lik)
        
if __name__ == '__main__':
    curl_webSev()
