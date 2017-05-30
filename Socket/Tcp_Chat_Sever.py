#!/usr/bin/env python
# -*- coding: utf-8 -*-

' Sever '

__author__ = 'Maloney'

import socket,select
def broadcast_data(sock,message):
    for s in CONNECTION_LIST:
        if s!=sock and s!=ss:
            try:
                s.send(message)
            except:
                s.close()
                CONNECTION_LIST.remove(s)

BUFFSIZE=4096
HOST=''
PORT=5000
CONNECTION_LIST=[]
ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
ss.bind((HOST,PORT))
ss.listen(10)

CONNECTION_LIST.append(ss)

print "chat sever started on port"+str(PORT)

while 1:
    r,w,e=select.select(CONNECTION_LIST,[],[])

    for sock in r:
        if sock==ss:
            cs,addr=ss.accept()
            CONNECTION_LIST.append(cs)
            print "client (%s,%s) connected"%addr
            broadcast_data(cs,"[%s:%s] entered room\n" %addr)
        else:
            try:
                data=sock.recv(BUFFSIZE)
                if data:
                    broadcast_data(sock,"\r"+'<'+str(sock.getpeername())+'>'+data)
            except:
                addr=sock.getpeername()
                broadcast_data(sock,"client (%s,%s) is offline"%addr)
                print "client (%s,%s) is offline"%addr
                sock.close()
                CONNECTION_LIST.remove(sock)
                continue
ss.close()