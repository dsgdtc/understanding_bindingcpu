#! /usr/bin/env python2
# -*- coding:utf-8 -*-
from socket import *
from fib import fib
from threading import Thread
from multiprocessing import Process
from multiprocessing import Event as PEvent
from bindingCpu import BindingCpu


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print('Connection', addr)
        #fib_handler(client)
        #Thread(target=fib_handler, args=(client,), daemon=True).start() #需要在python3下运行
        Thread(target=fib_handler, args=(client,)).start()

def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print('Closed')

def start_fib1():
    fib_server(('', 25002))

def start_fib2():
    fib_server(('', 25003))

if __name__ == '__main__':

#    p1 = Process(target=start_fib1, args=())
    p1 = Thread(target=start_fib1, args=())
    p1.start()
#    BindingCpu.affinity_cpu(p1, 8192)

#    p2 = Process(target=start_fib2, args=())
    p2 = Thread(target=start_fib2, args=())
    p2.start()
    #BindingCpu.affinity_cpu(p1, 4096)
    p1.join()
    p2.join()





