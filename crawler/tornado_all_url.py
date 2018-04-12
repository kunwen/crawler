import time, chardet,  datetime
from datetime import timedelta

try:
    from HTMLParser import HTMLParser
    from urlparse import urljoin, urldefrag
except ImportError:
    from html.parser import HTMLParser
    from urllib.parse import urljoin, urldefrag

from tornado import httpclient, gen, ioloop, queues
from functools import partial
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.log import gen_log

try:
    import urllib
except Exception:
    import urllib.request as urllib
    
from crawler.logger import logger

concurrency = 300

class NoQueueTimeoutHTTPClient(SimpleAsyncHTTPClient):
    def fetch_impl(self, request, callback):
        key = object()

        self.queue.append((key, request, callback))
        self.waiting[key] = (request, callback, None)

        self._process_queue()

        if self.queue:
            gen_log.debug("max_clients limit reached, request queued. %d active, %d queued requests." % (len(self.active), len(self.queue)))


httpclient.AsyncHTTPClient.configure(NoQueueTimeoutHTTPClient)

@gen.coroutine
def get_links_from_url(url, ftype, obj):
    try:
        if '://' not in url: 
                    if '//' == url[:1]:
                        pass
                    elif '/' ==url[0]:
                        proto, rest = urllib.splittype(url)
                        rest1, res2 = urllib.splithost(rest)
                        linksres = 'http://' + rest1 + url if rest1 else url
        begin = datetime.datetime.now()
        if ftype in url:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36', 'Referer':url}
            response = yield httpclient.AsyncHTTPClient().fetch(httpclient.HTTPRequest(url, headers=headers, validate_cert=False))
            html = response.body if isinstance(response.body, str) \
                else response.body.decode(chardet.detect(response.body).get('encoding'), "ignore")
            # 清洗数据
            if response.code==200:
                obj.scanpage((html, ftype, url))
                end = datetime.datetime.now()
                update_sql = "UPDATE  "+obj.ctable+" SET state=1 where url='%s'" % url 
                obj.curcheck.execute(update_sql)
	    # 清洗数据
            urls = [urljoin(url, remove_fragment(new_url))
                for new_url in get_links(html )]
            #插入记录
            for u in urls:
                insert_sql = "insert into "+obj.ctable+" (site,url) values (?,?)" 
                obj.curcheck.execute(insert_sql,(obj.table,u))
            obj.concheck.commit()

    except Exception as e:
        logger.error('错误信息：%s网页地址：%s' % (e, url))
        raise gen.Return([])

    raise gen.Return(urls)

#用于从一个包含片段的url中提取中真正的url.
def remove_fragment(url):       
    pure_url, frag = urldefrag(url)
    return pure_url


def get_links(html):
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
def main(base_url, ftype, obj):
    q = queues.Queue()
    start = time.time()
    fetching, fetched = set(), set()

    @gen.coroutine
    def fetch_url():
        current_url = yield q.get()
        try:
            if current_url in fetching:
                return

            fetching.add(current_url)
            urls = yield get_links_from_url(current_url, ftype, obj)
            fetched.add(current_url)

            for new_url in urls:
                # Only follow links beneath the base URL
                if ftype in new_url:
                    yield q.put(new_url)
        finally:
            q.task_done()

    @gen.coroutine
    def worker():
        while True:
            yield fetch_url()
	    
    q.put(base_url)
    
    for _ in range(concurrency):
        worker()
    yield q.join(timeout=timedelta(seconds=3600000))
    assert fetching == fetched
    print('Done in %d seconds, fetched %s URLs.' % (
        time.time() - start, len(fetched)))

def run_site(base_url, io_loop, ftype, obj):
    io_loop.run_sync(lambda: main(base_url, ftype, obj))


if __name__ == '__main__':
    io_loop.run_sync(lambda: main(base_url, ftype, obj))
