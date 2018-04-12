#!/usr/bin/env python
#coding: utf-8

'''
@auther: 王坤
create time：2017年4月21日
'''

import os, hashlib, platform, chardet, codecs
from os.path import join, getsize  
from bs4 import BeautifulSoup
from  subprocess import *
import time,re,psutil, requests
try:
    import urllib,urllib2
except Exception:
    import urllib.request as urllib
    import urllib.request as urllib2
    
import gevent
from gevent import monkey
monkey.patch_socket()

from crawler.logger import logger, logprint
from crawler.lang import LangagesofFamily
import crawler.content as content
from crawler.getdomain import SLD
from crawler.check import *
from crawler.tornado_all_url import run_site

import sys   
sys.setrecursionlimit(1000000)

class SiteUrl(object):
    def __init__(self, curcheck, concheck, cur, con, DEEP=1, xpath='backups/', tpath='./', langage=(['zh'], 'Chinese_Simp'), langurl = 'output/Chinese_Simp', ssize = 1):
        # 数据库
        self.curcheck = curcheck
        self.concheck = concheck
        self.cur = cur
        self.con = con
        self.table = tpath.split('/')[-2]
        self.ctable = langage[1]

        self.t=time.time()
        self.websiteurls={}
        self.DEEP = DEEP
        self.ssize = ssize
        self.xpath = xpath
        self.tpath = tpath
        self.langage = langage
        self.langurl = langurl
        self.allsiteU = []
        self.codelist = [(['pt'],'Breton'), (['qu'],'Afrikaans')]
        self.codekeys = ['pt', 'qu']
        self.codesuf = ['br', 'fa']

    def scanpage(self, param):
                import sys
                txtfile, ftype, links = param
                t, n, pageurls, Upageurls, res, langages=time.time(), 0, [], {}, [], LangagesofFamily()
                try:
                        '''
                        sitesize = PathSize().GetPathSize(self.langurl) # M
                        if float(sitesize) >= float(self.ssize):
                            logger.error('文件夹%s大小：%s, 要求最小%s' % (self.langurl, sitesize, self.ssize))
                            try:
                                requests.adapters.DEFAULT_RETRIES = 10  
                                requests.get('http://xn--cnq423f4sm.com:443/rescountry24/%s/%s/%s' % (get_mac_address(),self.langurl, sitesize), timeout=5)
                            except:
                                pass
                        else:'''
                        try:
                                # 创建text文件
                            m = hashlib.md5()
                            try:
                                m.update(links)
                            except Exception:
                                m.update(links.encode('utf-8'))
                        except urllib2.URLError as e:
                            pass
                        finally:
                            if isinstance(txtfile, bytes):
                                txtfile = txtfile.decode(chardet.detect(txtfile).get('encoding'), "ignore")
                            txtfile = content.main(txtfile)
                            tmpstr = txtfile.replace('\n', '')
                            txtfile = txtfile.encode('utf-8', "ignore")
                            if tmpstr:
                                lanres = langages.translate(txtfile, self.tpath +  m.hexdigest() + ".txt", self.langage, self.ssize, self)
                                if not lanres:
                                    logger.error('语言%s的类型不符：%s' % (self.langage[1], links))
                                else:
                                    pass #with codecs.open(self.xpath + ftype +'.log', 'a', "utf-8") as fp:
                                    #    fp.write('%s文件名称:%s.txt文件路径:%s\n' % (time.ctime(), m.hexdigest(), links))
                            else:
                                logger.warning("url网页清洗后为空：%s" % links)
                except Exception as err:
                        logger.error("网址%s连接失败原因: %s" % (str(links),str(err)))
                n+=1 
    
    def allsiteurl(self, base_url, ftype, io_loop, allurldir='siteurl/'):
        base_url = base_url[0]
        if '://' not in base_url: 
            if '//' == base_url[:1]:
                pass
            elif '/' ==base_url[0]:
                proto, rest = urllib.splittype(base_url)
                rest1, res2 = urllib.splithost(rest)
                base_url = 'http://' + rest1 + base_url if rest1 else base_url
            elif ftype in base_url.split('/')[0]:
                base_url = 'http://' + base_url
        run_site(base_url,io_loop, ftype, self)
    
if '__main__' == __name__:
    startUrlList = ['http://www.pricerunner.se']
    ftype = 'pricerunner.se'
    site_url = SiteUrl( DEEP=2, xpath='backups/', tpath='./', langage=(['sv'] ,'Swedish'), langurl = './', ssize = 5)
    site_url.allsiteU += startUrlList
    site_url.allsiteurl(startUrlList, ftype)
    with open(ftype + '.txt', 'w') as fp:
       for i in site_url.allsiteU:
           fp.writelines(i + '\n')
