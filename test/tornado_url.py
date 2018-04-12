#!/usr/bin/env python
# -*- coding:utf-8 -*-

from datetime import timedelta
from bs4 import BeautifulSoup
from tornado.httpclient import AsyncHTTPClient
from tornado import ioloop, gen, queues


@gen.coroutine
def fetch(url):
    response = yield AsyncHTTPClient().fetch(url, raise_error=False)
    raise gen.Return(response)

_q = queues.Queue()


@gen.coroutine
def run():
    try:
        url = yield _q.get()
        res = yield fetch(url)
        html = res.body
        soup = BeautifulSoup(html)
        print(str(soup.find('title')))
    finally:
        _q.task_done()


@gen.coroutine
def worker():
    while not _q.empty():
        yield run()


@gen.coroutine
def main():
    for i in range(73000, 73100):    # 放100个链接进去
        url = "http://www.jb51.net/article/%d.htm" % i
        yield _q.put(url)
    for _ in range(100):    # 模拟100个线程
        worker()
    yield _q.join(timeout=timedelta(seconds=30))


if __name__ == '__main__':
    print (ioloop.IOLoop.current().run_sync(main))
