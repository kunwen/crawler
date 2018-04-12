import pycurl
 
c = pycurl.Curl()
c.setopt(c.URL, 'http://www.baidu.com')
c.setopt(c.CONNECTTIMEOUT, 5)
c.setopt(c.TIMEOUT, 8)
c.setopt(c.COOKIEFILE, '')
c.setopt(c.FAILONERROR, True)
c.setopt(c.HTTPHEADER, ['Accept: text/html', 'Accept-Charset: UTF-8'])
try:
    c.perform()
 
    c.setopt(c.URL, 'http://baidu.com')
    c.setopt(c.POSTFIELDS, 'foo=bar&bar=foo')
    c.perform()
except pycurl.error, error:
    errno, errstr = error
    print 'An error occurred: ', errstr
