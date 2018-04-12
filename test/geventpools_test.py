#from gevent import pool 
#g = pool.Pool() 
#def a(): 
#    for i in xrange(100): 
#        g.spawn(b) 
#def b(): 
#    print 'b' 
#g.spawn(a) 
#g.join() 
#1import time
#1import gevent 
#1import gevent.monkey
#1import gevent.pool 
#1
#1def func(w):
#1    print w
#1    time.sleep(3)
#1gevent.monkey.patch_socket() 
#1
#1pool=gevent.pool.Pool(10)
#1
#1dataList = []
#1for i in range(300):
#1    print i
#1    dataList.append(pool.spawn(func,i))
#1
#1pool.join()
import gevent
from gevent.pool import Pool

pool = Pool(2)

def hello_from(n):
    print('Size of pool', len(pool))
    return ('Size of pool', len(pool))

print pool.map(hello_from, xrange(3))
