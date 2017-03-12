#!/usr/bin/env python
# -*- coding: utf-8 -*-

' Sever '

__author__ = 'Maloney'

import socket,traceback,sys
host='127.0.0.1'
port=9999

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((host,port))
s.listen(1)

CilentSock,CilentAddr=s.accept()

while 1:
    try:
        buf=CilentSock.recv(1024)
        if len(buf):
            print("he say :"+buf)
        data=raw_input("I say:")
        CilentSock.send(data)
    except:
        print("Dialogue Over")
        CilentSock.close()
        sys.exit(0)