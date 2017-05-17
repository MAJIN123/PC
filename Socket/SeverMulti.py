#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
from time import ctime
import threading
import re

HOST = ''
PORT = 21561
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock=socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

clients={}
chatwhit={}

def Deal(sock,user):
    while True:
        data=sock.recv(BUFSIZ)
        if data=='quit':
            del clients[user]
            sock.send(data)
            sock.close()
            print '%s logout'%user
            break
        elif re.match('to:',data) is not None:
            data=data[3:]
            if clients.has_key(data):
                chatwhit[sock]=clients[data]
                chatwhit[clients[data]]=sock
            else:
                sock.send('the user %s is not exist' %data)
        else:
            if chatwhit.has_key(sock):
                chatwhit[sock].send("[%s] %s: %s" %ctime(),user,data)
            else:
                sock.send('please input the user you want to chat with')

while True:
    print 'waiting for connection...'
    tcpCliSock,addr=tcpSerSock.accept()
    print '...connected from:',addr
    username=tcpCliSock.recv(BUFSIZ)
    print 'username is:',username
    if clients.has_key(username):
        tcpCliSock.send("Reuse")
        tcpCliSock.close()
    else:
        tcpCliSock.send("welcome!")
        clients[username]=tcpCliSock
        chat=threading.Thread(target=Deal,args=(tcpCliSock,username))
        chat.start()

tcpSerSock.close()
