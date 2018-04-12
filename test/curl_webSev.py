#!/usr/bin/python
#--coding:utf-8--#
#-------------------------------------------------------------------------------
# Name:        curl_webSev.py
#
# Author:      LiuSha
#
# Created:     12/15/2014
# Copyright:   (c) WDZJ-SA 2014
#-------------------------------------------------------------------------------
 
def curl_webSev(URL = 'www.ipython.me'):
    _Curl = pycurl.Curl()
    _Curl.setopt(pycurl.CONNECTTIMEOUT,5)
    _Curl.setopt(pycurl.TIMEOUT,5)
    _Curl.setopt(pycurl.NOPROGRESS,1)
    _Curl.setopt(pycurl.FORBID_REUSE,1)
    _Curl.setopt(pycurl.MAXREDIRS,1)
    _Curl.setopt(pycurl.DNS_CACHE_TIMEOUT,30)
    _Curl.setopt(pycurl.URL,URL)
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + "/content.txt",'w') as outfile:
            _Curl.setopt(pycurl.WRITEHEADER,outfile)
            _Curl.setopt(pycurl.WRITEDATA,outfile)
            _Curl.perform()
    except Exception as err:
        print ("exec error!\n\t%s" %err)
        sys.exit()
    print ("Http Code:\t%s" %_Curl.getinfo(_Curl.HTTP_CODE))
    print ("DNS lookup time:\t%s ms" %(_Curl.getinfo(_Curl.NAMELOOKUP_TIME) * 1000))
    print ("Create conn time:\t%s ms" %(_Curl.getinfo(_Curl.CONNECT_TIME) * 1000))
    print ("Ready conn time:\t%s ms" %(_Curl.getinfo(_Curl.PRETRANSFER_TIME) * 1000))
    print ("Tran Star time:\t%s ms" %(_Curl.getinfo(_Curl.STARTTRANSFER_TIME) * 1000))
    print ("Tran Over time:\t%s ms" %(_Curl.getinfo(_Curl.TOTAL_TIME) * 1000))
    print ("Download size:\t%d bytes/s" %_Curl.getinfo(_Curl.SIZE_DOWNLOAD))
    print ("HTTP header size:\t%d byte" %_Curl.getinfo(_Curl.HEADER_SIZE))
    print ("Avg download speed:\t%s bytes/s" %_Curl.getinfo(_Curl.SPEED_DOWNLOAD))
 
if __name__ == '__main__':
    import os
    import sys
    import time
    import pycurl
    if sys.argv[1]:
        curl_webSev(sys.argv[1])
    else:
        curl_webSev()
