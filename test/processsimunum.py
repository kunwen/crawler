#coding:utf-8
import random
from time import sleep
import sys
import multiprocessing
import os
#
#需求分析：有大批量数据需要执行，而且是重复一个函数操作（例如爆破密码），如果全部开始线程数N多，这里控制住线程数m个并行执行，其他等待
#
lock=multiprocessing.Lock()#一个锁
def a(x):#模拟需要重复执行的函数
  lock.acquire()#输出时候上锁，否则进程同时输出时候会混乱，不可读
  print '开始进程：',os.getpid(),'模拟进程时间:',x
  lock.release()
   
  sleep(x)#模拟执行操作
   
  lock.acquire()
  print '结束进程：',os.getpid(),'预测下一个进程启动会使用该进程号'
  lock.release()
list=[]
for i in range(10):#产生一个随机数数组，模拟每次调用函数需要的输入，这里模拟总共有10组需要处理
  list.append(random.randint(1,10))
   
pool=multiprocessing.Pool(processes=3)#限制并行进程数为3
pool.map(a,list)#创建进程池，调用函数a，传入参数为list,此参数必须是一个可迭代对象,因为map是在迭代创建每个进程
