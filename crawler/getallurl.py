#!/usr/bin/env python
#coding: utf-8

'''
@auther: 王坤
create time：2017年4月21日
'''

import os, hashlib, platform, chardet
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

import sys   
sys.setrecursionlimit(1000000)

class SiteUrl(object):
    def __init__(self, DEEP=1, xpath='backups/', tpath='./', langage=(['zh'], 'Chinese_Simp'), langurl = 'output/Chinese_Simp', ssize = 1):
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
        url, ftype = param
        try:
            reload(sys)
            sys.setdefaultencoding('utf8')
        except Exception:
            pass
        websiteurl=url
        t=time.time()
        n=0
        pageurls=[]
        Upageurls={}
        res = []
        langages = LangagesofFamily()
        try:
            sitesize = PathSize().GetPathSize(self.langurl) # M
            if float(sitesize) >= float(self.ssize):
                logger.error('文件夹%s大小：%s, 要求最小%s' % (self.langurl, sitesize, self.ssize))
                try:
                    requests.adapters.DEFAULT_RETRIES = 10  
                    requests.get('http://xn--cnq423f4sm.com:443/rescountry24/%s/%s/%s' % (get_mac_address(),self.langurl, sitesize), timeout=5)
                except:
                    pass
                return res
            requests.adapters.DEFAULT_RETRIES = 10
            html=requests.get(websiteurl,headers={'Referer': websiteurl}, timeout=20).text
        except Exception as err:
            logger.error( websiteurl)
            logger.error(err)
            return res
        soup=BeautifulSoup(html)
        pageurls=soup.find_all("a",href=True)
        for links in pageurls:
          linkshref = links.get("href").strip()
          # if websiteurl in links.get("href") and links.get("href") not in Upageurls and links.get("href") not in websiteurls:
          if linkshref and linkshref not in Upageurls:
            if '://' not in linkshref: 
                if '//' == linkshref[:1]:
                    pass
                elif '/' ==linkshref[0]:
                    proto, rest = urllib.splittype(websiteurl)
                    rest1, res2 = urllib.splithost(rest)
                    linksres = 'http://' + rest1 + linkshref if rest1 else linkshref
                    Upageurls[linksres]=0
                elif ftype in linkshref.split('/')[0]:
                    linksres = 'http://' + linkshref
                    Upageurls[linksres]=0
            elif ftype in linkshref:
                Upageurls[linkshref]=0
        self.allsiteU = list(set(Upageurls.keys()))
        for links in self.allsiteU:
          try:
            txtfile = ''
            # if 'Kazakh' == self.langage[1]:
            #     logger.error('文件夹：%s, 语言%s的编号%s' % (self.langurl, self.langage[1], ','.join(self.langage[0])))
            sitesize = PathSize().GetPathSize(self.langurl) # M
            if float(sitesize) >= float(self.ssize):
                logger.error('文件夹%s大小：%s, 要求最小%s' % (self.langurl, sitesize, self.ssize))
                try:
                    requests.adapters.DEFAULT_RETRIES = 10  
                    requests.get('http://xn--cnq423f4sm.com:443/rescountry24/%s/%s/%s' % (get_mac_address(),self.langurl, sitesize), timeout=5)
                except:
                    pass
                break
            # linksobj = requests.get(links,headers={'Referer': links})
            # linkcode = linksobj.status_code
            # linkcode = linksobj.code
            response = None
            try:
                req = urllib2.Request(links,headers={'Referer': links})
                req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
                response = urllib2.urlopen(req, timeout=20)
            # t2=time.time()
                Upageurls[links]=200
            #if 200 == linkcode:
                res.append(links)
                # 创建text文件
                m = hashlib.md5()
                try:
                    m.update(links)
                except Exception:
                    m.update(links.encode('utf-8'))
                # txtfile = content.main(linksobj.text)
                txtfile = response.read()
            except urllib2.URLError as e:
                #if hasattr(e, 'code'):
                #    logger.error("连接失败:返回编码%s" % e.code)
                #elif hasattr(e, 'reason'):
                #    logger.error("连接失败:原因 %s" % e.reason)
                #logger.error("网址%s" % links)
                linksobj = requests.get(links,headers={'Referer': links})
                #if platform.python_version()[0] == '3':
                #    linksobj = linksobj.encode(chardet.detect(linksobj).get('encoding'))
                linkcode = linksobj.status_code
                # 创建text文件
                m = hashlib.md5()
                try:
                    m.update(links)
                except Exception:
                    m.update(links.encode('utf-8'))
                if 200 == linkcode:
                    Upageurls[links]=200
                    res.append(links)
                    txtfile = linksobj.text
            finally:
                if isinstance(txtfile, bytes):
                    txtfile = txtfile.decode(chardet.detect(txtfile).get('encoding'), "ignore")
                txtfile = content.main(txtfile)
                tmpstr = txtfile.replace('\n', '')
                txtfile = txtfile.encode('utf-8', "ignore")
                if response:
                    response.close()
                if tmpstr:
                    lanres = langages.translate(txtfile, self.tpath +  m.hexdigest() + ".txt", self.langage, self.ssize)
                    if not lanres:
                        logger.error('语言%s的类型不符：%s' % (self.langage[1], links))
                    else:
                        with open(self.xpath + ftype +'.log', 'a') as fp:
                            fp.write('%s文件名称:%s.txt文件路径:%s\n' % (time.ctime(), m.hexdigest(), links))
                else:
                    logger.warning("url网页清洗后为空：%s" % links)
            # t1=time.time()
            # print t1-t2
          except Exception as err:
            logger.error("网址%s连接失败原因: %s" % (str(links),str(err)))
          n+=1
        logger.info("total is "+repr(n)+" links")
        logger.info(str(time.time()-t))
        return res
    
    def allChildUrl(self, argsList, ftype, allurldir):
        urlList = []
        self.DEEP -=1
        logger.info(self.DEEP)
        sitesize = PathSize().GetPathSize(self.langurl) # M
        if float(sitesize) >= float(self.ssize):
            logger.error('文件夹%s大小：%s, 要求最小%s' % (self.langurl, sitesize, self.ssize))
            try:
                requests.adapters.DEFAULT_RETRIES = 10  
                requests.get('http://xn--cnq423f4sm.com:443/rescountry24/%s/%s/%s' % (get_mac_address(),self.langurl, sitesize), timeout=5)
            except:
                pass
            
        # 提高IO并发量
        # jobs = [gevent.spawn(self.scanpage, args, ftype) for args in argsList]
        # gevent.joinall(jobs)
        # 使用协程池 
        #dataList = []
        pool=gevent.pool.Pool(500)
        #for args in argsList:
        #    dataList.append(pool.spawn(self.scanpage, args, ftype))
        #argsList = pool.join()
        #print (argsList)
        argsList = pool.imap(self.scanpage, [ (args, ftype) for args in argsList])
        
        urlList = []
        for args in argsList:
        #    argsres = self.scanpage(args, ftype)
        #    if argsres:
        #    if args
        #        urlList += argsres
                urlList +=args
        
        if ftype:
            with open(allurldir + ftype + '.txt', 'w') as fp:
               for i in urlList:
                   fp.writelines(i + '\n')
        if self.DEEP<=0:
            urlList = []
        return urlList
    
    def allsiteurl(self, singleUrlsL, ftype, allurldir='siteurl/'):
        if not singleUrlsL or psutil.virtual_memory().percent >=90.0 :
            return True
        else:
            # print  psutil.virtual_memory().percent
            singleUrlsL = self.allChildUrl(singleUrlsL, ftype, allurldir)
            # singleUrlsL = list(set(singleUrlsL).difference(set(self.allsiteU)))
            # self.allsiteU += singleUrlsL
            res = self.allsiteurl(singleUrlsL, ftype)
            return res
    
if '__main__' == __name__:
    startUrlList = ['http://www.pricerunner.se']
    ftype = 'pricerunner.se'
    site_url = SiteUrl( DEEP=2, xpath='backups/', tpath='./', langage=(['sv'] ,'Swedish'), langurl = './', ssize = 5)
    site_url.allsiteU += startUrlList
    site_url.allsiteurl(startUrlList, ftype)
    with open(ftype + '.txt', 'w') as fp:
       for i in site_url.allsiteU:
           fp.writelines(i + '\n')
