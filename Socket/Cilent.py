#!/usr/bin/env python
# -*- coding: utf-8 -*-

' Cilent '

__author__ = 'Maloney'

import socket,sys,time
host='127.0.0.1'
port=9999

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.connect((host,port))
except socket.gaierror,e:
    print('Address-related error to srver:%s'%e)
    sys.exit(1)

while(1):
    try:
        data=raw_input("I say: ")
        time.sleep(1)
        s.send(data)
        buf=s.recv(1024)
        if len(buf):
            print("he say: "+buf)
    except:
        print("Dialogue Over")
        s.close()
        sys.exit(0)


