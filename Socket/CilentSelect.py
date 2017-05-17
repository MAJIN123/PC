#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *
from time import ctime
import select
import sys

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
input = [tcpCliSock, sys.stdin]

while True:
    readyInput, readyOutput, readyException = select.select(input, [], [])
    for indata in readyInput:
        if indata == tcpCliSock:
            data = tcpCliSock.recv(BUFSIZ)
            print data
            if data == '88':
                break
        else:
            data = raw_input('>')
            if data == '88':
                tcpCliSock.send('%s' % (data))
                break
            tcpCliSock.send('[%s] %s' % (ctime(), data))
    if data == '88':
        break
tcpCliSock.close()
# import socket
# import select
# import sys
#
# HOST='localhost'
# PORT=21567
# BUFFSIZE=1024
# ADDR=(HOST,PORT)
#
# ss=socket.socket()
# ss.connect(ADDR)
#
# inputs=[ss,sys.stdin]
#
# while True:
#     rs,ws,es=select.select(inputs,[],[])
#     for r in rs:
#         if(r==ss):
#             data=ss.recv(BUFFSIZE)
#             print("from sever:")
#             if(data=='88'):
#                 break
#         else:
#             data=raw_input('>')
#             if(data=='88'):
#                 ss.send(data)
#                 break
#             ss.send(data)
# ss.close()