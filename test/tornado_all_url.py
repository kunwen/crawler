import time
from datetime import timedelta

try:
    from HTMLParser import HTMLParser
    from urlparse import urljoin, urldefrag
except ImportError:
    from html.parser import HTMLParser
    from urllib.parse import urljoin, urldefrag

from tornado import httpclient, gen, ioloop, queues
from functools import partial

try:
    import urllib,urllib2
except Exception:
    import urllib.request as urllib
    import urllib.request as urllib2

from crawler import tornado_url

#all_url = []
concurrency = 30


@gen.coroutine
def get_links_from_url(url, ftype):
    """Download the page at `url` and parse it for links.

    Returned links have had the fragment after `#` removed, and have been made
    absolute so, e.g. the URL 'gen.html#tornado.gen.coroutine' becomes
    'http://www.tornadoweb.org/en/stable/gen.html'.
    """
    try:
        if '://' not in url: 
                    if '//' == url[:1]:
                        pass
                    elif '/' ==url[0]:
                        proto, rest = urllib.splittype(url)
                        rest1, res2 = urllib.splithost(rest)
                        linksres = 'http://' + rest1 + url if rest1 else url
        if ftype in url:
            response = yield httpclient.AsyncHTTPClient().fetch(url)
        #all_url.append( url)

            html = response.body if isinstance(response.body, str) \
                else response.body.decode()
            urls = [urljoin(url, remove_fragment(new_url))
                for new_url in get_links(html, ftype)]
            # 清洗数据
            if response.code==200:
                t, n, pageurls, Upageurls, res, langages=time.time(), 0, [], {}, [], LangagesofFamily()
                try:
                    sitesize = PathSize().GetPathSize(self.langurl) # M
                    if float(sitesize) >= float(self.ssize):
                        logger.error('文件夹%s大小：%s, 要求最小%s' % (self.langurl, sitesize, self.ssize))
                        try:
                            requests.adapters.DEFAULT_RETRIES = 10  
                            requests.get('http://xn--cnq423f4sm.com:443/rescountry24/%s/%s/%s' % (get_mac_address(),self.langurl, sitesize), timeout=5)
                        except:
                            pass
                    else:
                        try:
                                # 创建text文件
                            m = hashlib.md5()
                            try:
                                m.update(links)
                            except Exception:
                                m.update(links.encode('utf-8'))
                            txtfile = response.read()
                        except urllib2.URLError as e:
                            pass
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
                                    with codecs.open(self.xpath + ftype +'.log', 'a') as fp:
                                        fp.write('%s文件名称:%s.txt文件路径:%s\n' % (time.ctime(), m.hexdigest(), links))
                            else:
                                logger.warning("url网页清洗后为空：%s" % links)
                except Exception as err:
                        logger.error("网址%s连接失败原因: %s" % (str(links),str(err)))
                n+=1 
    	# 清洗数据

    except Exception as e:
        print('Exception: %s %s' % (e, url))
        raise gen.Return([])

    raise gen.Return(urls)

#用于从一个包含片段的url中提取中真正的url.
def remove_fragment(url):       
    pure_url, frag = urldefrag(url)
    return pure_url


def get_links(html, ftype):
    class URLSeeker(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.urls = []

	#从所有a标签中提取中href属性。
        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get('href')
            if href and tag == 'a':
                self.urls.append(href)

    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls


@gen.coroutine
def main(base_url, ftype):
    q = queues.Queue()
    start = time.time()
    fetching, fetched = set(), set()

    @gen.coroutine
    def fetch_url():
        current_url = yield q.get()
        try:
            if current_url in fetching:
                return

            print('fetching %s' % current_url)
            fetching.add(current_url)
            urls = yield get_links_from_url(current_url, ftype)
            fetched.add(current_url)

            for new_url in urls:
                # Only follow links beneath the base URL
                if new_url.startswith(base_url):
                    yield q.put(new_url)

        finally:
            q.task_done()

    @gen.coroutine
    def worker():
        while True:
            yield fetch_url()

    q.put(base_url)

    # Start workers, then wait for the work queue to be empty.
    for _ in range(concurrency):
        worker()
    yield q.join(timeout=timedelta(seconds=3600))
    assert fetching == fetched
    assert len(fetching)<=100000
    print('Done in %d seconds, fetched %s URLs.' % (
        time.time() - start, len(fetched)))

def run_site(base_url, io_loop, ftype):
    #main = partial(main, base_url)
    io_loop.run_sync(lambda: main(base_url, ftype))


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    ioloop.IOLoop.current().run_sync(main)
