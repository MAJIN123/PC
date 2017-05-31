import cookielib
import urllib2

cookie=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response=opener.open("http://www.baidu.com")
for s in cookie:
    print cookie