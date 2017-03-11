#!/usr/bin/env python
# -*- coding: utf-8 -*-

' process'

__author__ = 'Maloney'
from multiprocessing import Queue,Process
import os,time,random
print('Process (%s) start' %os.getpid())

pid=os.fork()
if pid==0:
    print('I am child process (%s) and my parent is (%s)'%(os.getpid(),os.getppid()))
else:
    print('I(%s)just created a process (%s)'%(os.getpid(),pid))
start=time.time()
time.sleep(random.random())
end=time.time()
print('%s'%(end-start))

#queue实现进程通信
def write(q):
    for s in ['a','s','f']:
        q.put(s)
        print('put %s in queue'%s)
        time.sleep(random.random())
def read(q):
    while True:
        p=q.get(True)
        print('get %s from queue'%p)
if __name__=='__main__':
    q=Queue()
    pw=Process(target=write,args=(q,))
    pr=Process(target=read,args=(q,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()