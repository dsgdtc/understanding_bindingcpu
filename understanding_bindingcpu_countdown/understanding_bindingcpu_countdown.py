# -*- coding:utf-8 -*-

from threading import Thread
from threading import Event as TEvent
from multiprocessing import Process
from multiprocessing import Event as PEvent
import affinity
from bindingCpu import BindingCpu

#import utility
#utility.SetAffinity(1)

from timeit import Timer

import sys
sys.setcheckinterval(100) #(100000)

def countdown(n,event):
    while n > 0:
        n -= 1
    event.set()

def io_op(n,event,filename):
    f = open(filename,'w')
    while not event.is_set():
        f.write('hello,world')
    f.close()

def t1(COUNT=100000000):
    
    event = TEvent()
    thread1 = Thread(target=countdown,args=(COUNT,event))
    thread1.start()
    thread1.join()

def t1_bindingcpu1():
    COUNT=100000000
    p1 = Process(target=t1, args=(COUNT//2,))
    p1.start()
    BindingCpu.affinity_cpu(p1, 1)
    p1.join()

def t1_bindingcpu16():
    COUNT=100000000
    p1 = Process(target=t1, args=(COUNT//2,))
    p1.start()
    BindingCpu.affinity_cpu(p1, 32768)
    p1.join()

# 单核多线程的性能比多核多线程要好
def t2():
    COUNT=100000000
    event = TEvent()
    thread1 = Thread(target=countdown,args=(COUNT//2,event))
    thread2 = Thread(target=countdown,args=(COUNT//2,event))
    thread1.start(); thread2.start()
    thread1.join(); thread2.join()

def t2_bindingcpu():
    p1 = Process(target=t2, args=())
    p1.start()
    BindingCpu.affinity_cpu(p1, 2)
    p1.join()

def t3():
    COUNT=100000000
    event = PEvent()
    p1 = Process(target=countdown,args=(COUNT//2,event))
    p2 = Process(target=countdown,args=(COUNT//2,event))
    p1.start()
    p2.start()
    p1.join() 
    p2.join()

def t3_bindingcpu():
    COUNT=100000000
    event = PEvent()
    p1 = Process(target=countdown,args=(COUNT//2,event))
    p2 = Process(target=countdown,args=(COUNT//2,event))
    p1.start()
    BindingCpu.affinity_cpu(p1, 4)
    p2.start()
    BindingCpu.affinity_cpu(p2, 8)
    p1.join() 
    p2.join()


def t4():
    COUNT=100000000
    event = TEvent()
    thread1 = Thread(target=countdown,args=(COUNT,event))
    thread2 = Thread(target=io_op,args=(COUNT,event,'thread.txt'))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

def t4_bindingcpu():
    p1 = Process(target=t4, args=())
    p1.start()
    BindingCpu.affinity_cpu(p1, 16)
    p1.join()


def t5():
    COUNT=100000000
    event = PEvent()
    p1 = Process(target=countdown,args=(COUNT,event))
    p2 = Process(target=io_op,args=(COUNT,event,'process.txt'))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

def t5_bindingcpu():
    COUNT=100000000
    event = PEvent()
    p1 = Process(target=countdown,args=(COUNT,event))
    p2 = Process(target=io_op,args=(COUNT,event,'process.txt'))
    p1.start()
    BindingCpu.affinity_cpu(p1, 256)
    p2.start()
    BindingCpu.affinity_cpu(p2, 512)
    p1.join()
    p2.join()


if __name__ == '__main__':


    t = Timer(t1)
    print('t1test: countdown in one thread:%f'%(t.timeit(1),))
    t = Timer(t1_bindingcpu1)
    print('t1test: bindingcpu1  countdown in one thread:%f'%(t.timeit(1),))
    t = Timer(t1_bindingcpu16)
    print('t1test: bindingcpu16 countdown in one thread:%f'%(t.timeit(1),))
    print '-'*50

    t = Timer(t2)
    print('t2test: countdown use two thread:%f'%(t.timeit(1),))
    t = Timer(t2_bindingcpu)
    print('t2test: bindingcpu countdown use two thread:%f'%(t.timeit(1),))
    print '-'*50

    t = Timer(t3)
    print('t3test: countdown use two Process:%f'%(t.timeit(1),))
    t = Timer(t3_bindingcpu)
    print('t3test: bindingcpu countdown use two Process:%f'%(t.timeit(1),))
    print '-'*50
 
    t = Timer(t4)
    print('t4test: countdown in one thread with io op in another thread:%f'%(t.timeit(1),))
    t = Timer(t4_bindingcpu)
    print('t4test: bindingcpu countdown in one thread with io op in another thread:%f'%(t.timeit(1),))
    print '-'*50

    t = Timer(t5)
    print('t5test: countdown in one process with io op in another process:%f'%(t.timeit(1),))
    t = Timer(t5_bindingcpu)
    print('t5test: bindingcpu countdown in one process with io op in another process:%f'%(t.timeit(1),))
