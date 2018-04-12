#!/usr/bin/env python
#coding: utf-8

'''
@auther: 王坤
create time：2017年4月21日
'''

import os, logging  
import logging.config  
  
# 创建logs文件夹
if not os.path.exists('logs/'):
   os.makedirs('logs/')
logging.config.fileConfig('crawler/logging.conf')  
logger = logging.getLogger('main')
logprint = logging.getLogger('root')
#logger = logging.getLogger('main.mod')
#logger = logging.getLogger('main.mod.submod')  
