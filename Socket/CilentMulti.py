#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
from time import ctime
import threading
import re

HOST = 'localhost'
PORT = 21572
BUFSIZ = 1024
ADDR = (HOST, PORT)
threads = []

tcpCilSock=socket(AF_INET,SOCK_STREAM)
tcpCilSock.connect(ADDR)

def Send(sock,test):
    while True:
        data=raw_input('>')
        sock.send(data)
        if data=='quit':
            break

def Recv(sock,test):
    while True:
        data=sock.recv(BUFSIZ)
        if data=='quit':
            sock.close()
            break
        print data
print 'please input your username:'
username=raw_input()
tcpCilSock.send(username)
data=tcpCilSock.recv(BUFSIZ)
if data=='Reuse':
    print 'the username has been used!'
else:
    print 'welcome!'
    chat=threading.Thread(target=Send,args=(tcpCilSock,None))
    threads.append(chat)
    chat=threading.Thread(target=Recv,args=(tcpCilSock,None))
    threads.append(chat)
    for i in range(len(threads)):
        threads[i].start()
    threads[0].join()

