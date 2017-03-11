#!/usr/bin/env python
# -*- coding: utf-8 -*-

' function '

__author__ = 'Maloney'
import os
print(os.uname())
def reverse_cmp(x,y):
    if(x<y):
        return 1
    if(x>y):
        return -1
    else:
        return 0
def cmp_ignore_case(s1,s2):
    a=s1.upper()
    b=s2.upper()
    if(a<b):
        return -1
    if(a>b):
        return 1
    return 0
print(sorted([3,7,1,9],reverse_cmp))
L=['Ss','dd','aa']
print(sorted(L,cmp_ignore_case))
#求和sum
def Sum(*args):
    ax=0
    for x in args:
        ax+=x
    return ax
#不需要立即求和，根据需要求和
def lazy_Sum(*args):
    def sum():
        ax=0
        for x in args:
            ax+=x
        return ax
    return sum
print(lazy_Sum(1,3,5)())
#闭包？
def count():
    fs=[]
    for i in range(1,4):
        def f():
            return i*i
        fs.append(f)#注意是f而不是f()
    return fs
f1,f2,f3=count()
print(f1())




