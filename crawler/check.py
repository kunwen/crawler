#!/usr/bin/env python
#coding: utf-8

'''
@auther: 王坤
create time：2017年4月21日
'''

import os, hashlib, platform
from os.path import join, getsize  
from  subprocess import *

# 获取本机mac 
def get_mac_address(): 
    import hashlib
    import uuid
    m = hashlib.md5()
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    mac = ":".join([mac[e:e+2] for e in range(0,11,2)])
    if platform.python_version()[0] == '3':
        mac = mac.encode('utf-8')
    m.update(mac)
    return m.hexdigest()

def getpathsize(path):  
   size = 0
   for root, dirs, files in os.walk(path):  
      size += sum([getsize(join(root, name)) for name in files])  
   return size  

class PathSize(object):
    def __init__(self):
        pass

    def GetPathSize(self, strPath):  
        nTotalSize = 0
        sysstr = platform.system()
        if(sysstr =="Windows"):
          nTotalSize = getpathsize(strPath)
        elif(sysstr == "Linux"):
          nTotalSize = check_output(["du", "-sb" , strPath]).strip().split('\t')[0]
        else:
          nTotalSize = check_output(["du", "-sb" , strPath]).strip().split('\t')[0]
        return float(nTotalSize)/1024/1024
