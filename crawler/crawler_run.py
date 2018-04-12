#!/usr/bin/env python
#coding: utf-8

'''
@auther: 王坤
create time：2017年4月21日
'''

import time, logging
import os, glob, requests, shutil
try:   
    import httplib as http
except Exception:
    import http.client as http
from os.path import join, getsize  
import multiprocessing, threadpool 

from crawler.getdomain import SLD
from crawler.getallurl import  SiteUrl
from crawler.lang import LangagesofFamily
from crawler.logger import logger
from crawler.check import *

sld = SLD()
# lock=multiprocessing.Lock()#一个锁

mainUrl, confpath, urldir, xfile = 'output/', 'conf/', 'siteurl/', 'backups/'

def get_webservertime(host):
    conn=http.HTTPConnection(host)
    conn.request("GET", "/")
    r=conn.getresponse()
    #r.getheaders() #获取所有的http头
    ts=  r.getheader('date') #获取http头date部分
    #将GMT时间转换成北京时间
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ttime=time.localtime(time.mktime(ltime)+8*60*60)
    dat="%u%02u%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    tm="%02u%02u%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
    return (dat,tm)

def get_mac_address(): 
    import hashlib
    import uuid
    m = hashlib.md5()
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    m.update(":".join([mac[e:e+2] for e in range(0,11,2)]))
    return m.hexdigest()

def main():
    global mainUrl

    allfile = glob.glob(confpath + '*.conf')
    ssize = input("* 请输入每种语言下载量 (默认1 单位:M)>>>")  
    deep = input("* 请输入每个网站最大爬取深度 默认3 >>>")  
    threadnum = input("* 请输入每门语言同一时间爬取的网站个数（线程数） 默认3(谨慎修改，可直接按回车)>")  
    if not deep:deep=3
    if not threadnum:threadnum=3
    if not ssize:ssize=1
    # 期限设置
    nowdate = get_webservertime('www.baidu.com')
    try:
        req = requests.get('http://xn--cnq423f4sm.com:443/country24/'+ get_mac_address(), timeout=5)
    except:
        req = ''
    if req and (not nowdate or int(nowdate[0]) >= eval(req.text)):
        return logger.error('已过有效期！')

    langages = LangagesofFamily()
    # 网站地址全集
    if not os.path.exists(urldir):
        os.makedirs(urldir)
    # 创建html文件
    if not os.path.exists(xfile):
       os.makedirs(xfile)

    for i in langages.lanclass:
       if os.path.exists(confpath+i[1]+'.conf'):
            mainUrl = 'output/' + i[1] + '/'
            if not os.path.exists(mainUrl):
                os.makedirs(mainUrl)
            logger.info( '生成的文件将要输出到这个目录下：%s ！' % mainUrl)
            lik = i[0]
     
            with open(confpath+i[1]+'.conf','r') as fp:
                outf = fp.readlines()
            allOneLangageSite(outf, i, mainUrl, langages, deep, threadnum, ssize)

def allOneLangageSite(outf, lik, mainUrl, langages, deep, threadnum, ssize):
    n, sn = 1, 1
    # pool=multiprocessing.Pool(processes=5) #限制并行进程数为5
    # 多线程
    pool_args = []
    pool = threadpool.ThreadPool(int(threadnum)) 
    print ('starting at:%s' % time.strftime( '%Y-%m-%d %H:%M:%S' , time.localtime() ))
    
    for j in outf:
        conflist = j.strip().replace('\n', '').replace('\r', '').split('=')
        if len(conflist)>=3:
            f = conflist[2]
            if not '://' in f:
                f = 'http://' + f
            startUrlList = [f]
            try:
                ftype = sld.get_second_level_domain(j[2])
            except Exception as e:
                logger.error("url获取域名问题：%s !" % e)
                ftype = ''.join(f.split("://")[1:]).split("/")[0]
            finally:
                if not ftype:
                    ftype = ''.join(f.split("://")[1:]).split("/")[0]
                logger.error('%s域名:%s' % (lik[1], ftype))
                # pool.apply_async(craw_run, (startUrlList,ftype, lik,langages, mainUrl, deep, ssize, conflist))
                args=[startUrlList,ftype, lik,langages, mainUrl, deep, ssize, conflist]
                pool_args.append( (args, None))
                n += 1
                # if runres:  
                #     sn +=1
                #     logger.info(u'语言%s检索到了%s个网站，有效的网站有%s个！' % (lik[1], str(n), str(sn)))
        else:
            logger.error('配置文件%s的这一行%s有问题！' % (i[1]+'.conf', j))
    # pool.close()
    # pool.join()
    reqs = threadpool.makeRequests(craw_run, pool_args)  
    [pool.putRequest(req) for req in reqs]  
    pool.wait() 

def craw_run(startUrlList, ftype, lik, langages, mainUrl, deep, ssize, conflist):
    sitesize = PathSize().GetPathSize(mainUrl) # M
    if float(sitesize) >= float(ssize):
        return False
    tfile = mainUrl + str(conflist[0]) + '/'
    # 创建text文件目录
    if not os.path.exists(tfile):
        os.makedirs(tfile)
    site_url = SiteUrl(int(deep), xfile, tfile, lik, mainUrl, ssize)
    site_url.allsiteU += startUrlList
    site_url.allsiteurl(startUrlList, ftype, urldir)
    if not os.listdir(tfile):
        shutil.rmtree(tfile)
        return False
    else:
        return True

if '__main__' == __name__:
    main() 
