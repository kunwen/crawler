#!/usr/bin/env python
#coding: utf-8

'''
@auther: 王坤
create time：2017年4月21日
'''

import time, logging, codecs
import os, glob, requests, shutil
try:   
    import httplib as http
except Exception:
    import http.client as http
from os.path import join, getsize  
import multiprocessing, threadpool
from tornado import ioloop

from crawler.getdomain import SLD
from crawler.getallurl import  SiteUrl
from crawler.lang import LangagesofFamily
from crawler.logger import logger
from crawler.check import *

import sqlite3

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

def main():
    global mainUrl

    allfile = glob.glob(confpath + '*.conf')
    ssize = input("* 请输入每种语言下载量 (默认1 单位:M)>>>")   
    deep, threadnum, ssize=6, 1, 1
    # 期限设置
    try:
        nowdate = get_webservertime('www.baidu.com')
        req = requests.get('http://xn--cnq423f4sm.com:443/country24/'+ get_mac_address(), timeout=5)
        if req and (not nowdate or int(nowdate[0]) >= eval(req.text)):
            return logger.error('已过有效期！')
    except:
        pass
    
    langages = LangagesofFamily()
    # 网站地址全集
    if not os.path.exists(urldir):
        os.makedirs(urldir)
    # 创建html文件
    if not os.path.exists(xfile):
       os.makedirs(xfile)

    checkurl = urldir + "siteurl.db"
    concheck = sqlite3.connect(checkurl)
    curcheck = concheck.cursor() 

    for i in langages.lanclass:
       if os.path.exists(confpath+i[1]+'.conf'):
            mainUrl = 'output/' + i[1] + '/'
            #if not os.path.exists(mainUrl):
            #    os.makedirs(mainUrl)
            logger.info( '生成的文件将要输出到这个目录下：%s ！' % mainUrl)
            lik = i[0]
     
            with codecs.open(confpath+i[1]+'.conf','r', "utf-8") as fp:
                outf = fp.readlines()
            crt_tb_sql = "create table if not exists "+ i[1] + """(
                              id integer primary key autoincrement unique not null,
                              site varchar(100),
                              url varchar(100),
                              state integer default 0
                            );
                            """
            curcheck.execute(crt_tb_sql)
            #连接数据库
            con = sqlite3.connect('output/' + i[1]+'.db')
            cur = con.cursor()       
            concheck.commit()   
            allOneLangageSite(outf, i, mainUrl, langages, deep, threadnum, ssize, curcheck, concheck, cur, con)
            con.commit()
            con.close()
            cur.close()
    concheck.commit()
    concheck.close()
    curcheck.close()

def allOneLangageSite(outf, lik, mainUrl, langages, deep, threadnum, ssize, curcheck, concheck, cur, con):
    n, sn,  = 0, 1
    pool_args = []
    pool = threadpool.ThreadPool(int(threadnum)) 
    print ('starting at:%s' % time.strftime( '%Y-%m-%d %H:%M:%S' , time.localtime() ))
    io_loop = ioloop.IOLoop.current()
    for j in outf:
        conflist = j.strip().replace('\n', '').replace('\r', '').split('=')
        n += 1
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
                print ('%s - %s域名:%s' % (time.ctime(), lik[1], ftype))

                # 一个网站一张表
                crt_tb_sql = "create table if not exists t"+ conflist[0] +"""(
                              id integer primary key autoincrement unique not null,
                              site varchar(200),
                              content text
                            );
                            """
                cur.execute(crt_tb_sql)
                #插入记录
                insert_sql = "insert into "+lik[1]+" (site,url) values (?,?)" 
                curcheck.execute(insert_sql,( conflist[0],conflist[2]))
                concheck.commit()
                craw_run(startUrlList,ftype, lik,langages, mainUrl, deep, ssize, conflist, io_loop, curcheck, concheck, cur, con)
                update_sql = "UPDATE  "+lik[1]+" SET state=1 where id='%s'" % str(curcheck.lastrowid)
                curcheck.execute(update_sql)
                concheck.commit()
        else:
            logger.error('配置文件%s的第%s行有问题！' % (lik[1]+'.conf', n))

def craw_run(startUrlList, ftype, lik, langages, mainUrl, deep, ssize, conflist, io_loop, curcheck, concheck, cur, con):
    sitesize = PathSize().GetPathSize(mainUrl) # M
    if float(sitesize) >= float(ssize):
        return False
    tfile = mainUrl + str(conflist[0]) + '/'
    # 创建text文件目录
    if not os.path.exists(tfile):
        os.makedirs(tfile)
    site_url = SiteUrl(curcheck, concheck, cur, con,int(deep), xfile, tfile, lik, mainUrl, ssize)
    site_url.allsiteU += startUrlList
    site_url.allsiteurl(startUrlList, ftype, io_loop, urldir)
    if not os.listdir(tfile):
        shutil.rmtree(tfile)
        return False
    else:
        return True

if '__main__' == __name__:
    main() 
