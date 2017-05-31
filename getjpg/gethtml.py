#!/usr/bin/env python
# -*- coding: utf-8 -*-

' gethtml '

__author__ = 'Maloney'

import urllib
import urllib2

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html
url = 'http://www.someserver.com/cgi-bin/register.cgi'
#html = getHtml("https://www.zhihu.com/question/27830729")
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
data={}
data['name']='mj'
data['location']='suzhou'
data['language']='majin'
headers={'User_Agent':user_agent}
values=urllib.urlencode(data)
req=urllib2.Request(url,values,headers)
response=urllib2.urlopen(req)
page=response.read()
print page
