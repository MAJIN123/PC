#!/usr/bin/env python
# -*- coding: utf-8 -*-

' Client '

__author__ = 'Maloney'
import socket,select,string,sys
def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()
host='localhost'
port=5000
s=socket.socket()
s.settimeout(2)

try:
    s.connect((host,port))
except:
    print "Unable to connect"
    sys.exit()
print 'Connected to the remote host.Start sending message'
prompt()

while 1:
    socket_list=[sys.stdin,s]
    r,w,e=select.select(socket_list,[],[])

    for sock in r:
        if sock==s:
            data=sock.recv(4096)
            if not data:
                print '\nDisconnected from chat sever'
                sys.exit()
            else:
                sys.stdout.write(data)
                prompt()
        else:
            msg=sys.stdin.readline()
            s.send(msg)
            prompt()
