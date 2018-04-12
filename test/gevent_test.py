from gevent import monkey; monkey.patch_all()
import gevent
try:
    import urllib,urllib2
except Exception:
    import urllib.request as urllib
    import urllib.request as urllib2

def f(url,x):
    print('%sGET: %s' % (x,url))
    resp = urllib2.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))

gevent.joinall([
        gevent.spawn(f, 'https://www.python.org/',1),
        gevent.spawn(f, 'https://www.yahoo.com/', 2),
        gevent.spawn(f, 'https://github.com/',3),
])
#>>> import gevent
#
#>>> from gevent import socket
#
#>>> urls = ['www.google.com.hk','www.example.com', 'www.python.org'  ]
#
#>>> jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
#
#>>> gevent.joinall(jobs, timeout=2)
#
#>>> [job.value for job in jobs]
#
#['74.125.128.199', '208.77.188.166', '82.94.164.162']
