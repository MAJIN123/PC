#!/usr/bin/env python
# -*- coding: utf-8 -*-

' test 1 '

__author__ = 'Maloney'
import os
##读文件的字符串到sts（是个list）
filename=('1','2','3','4','5','6','7','8','9','10')
sts=[]
for i in range(10):
    with open (filename[i],'r') as f:
        lines=f.readlines()
        for line in lines:
            for st in line.split():
                st=filter(str.isalpha,st)
                sts.append(st)
db={}
for word in sts:
    if word in db:
        db[word]=db[word]+1
    else:
        db[word]=1
print(db)

