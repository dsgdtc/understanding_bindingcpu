#! /usr/bin/env python2
# -*- coding:utf-8 -*-
#perf1.py
from socket import *
from threading import Thread
import time

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25003))

n = 0

def monitor():
    global n
    while True:
        time.sleep(1)
        print(n, 'reqs/sec')
        n = 0
Thread(target=monitor).start()


while True:
    start = time.time()
    sock.send(b'10')
    resp = sock.recv(100)
    end = time.time()
    n += 1

#代码非常简单，通过全局变量n来统计qps(req/sec 每秒请求数)
