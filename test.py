# -*- coding: utf-8 -*-
# 302 Found 是HTTP协议中的一个状态码(Status Code)。可以简单的理解为该资源原本确实存在，但已经被临时改变了位置；或者换个说法，就是临时的存在于某个临时URL下。通常会发送Header来暂时重定向到新的新位置。
# 对于从百度爬取的加密的url，进行requests.get()时不允许跳转（allow_redirects=False）。然后针对这两类服务器回复分别处理。
# http 302跳转：从headers中的'location'可以获得原始url；
# http 200回复：从content中通过正则表达式获取原始url
# 在Python的string前面加上‘r’， 是为了告诉编译器这个string是个raw string，不要转意backslash '\' 。 例如，\n 在raw string中，是两个字符，\和n， 而不会转意为换行符。由于正则表达式和 \ 会有冲突，因此，当一个字符串使用了正则表达式后，最好在前面加上'r'。


import re
import requests
from pyquery import PyQuery as pq
import sys


class BaiduSearchSpider(object):

    def __init__(self, search_text):
        self.url = "http://www.baidu.com/baidu?wd=%s" % search_text
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"}
        self._page = None
    
    @property  # @property装饰器就是负责把一个方法变成属性调用的
    def page(self):
        if not self._page:
            r = requests.get(self.url, headers=self.headers)
            r.encoding = 'utf-8'
            self._page = pq(r.text)
        return self._page
    
    @property
    def baidu_urls(self):
        return [(site.attr('href'), site.text().encode('utf-8')) for site in self.page('div.result.c-container h3.t a').items()]
    
    @property    # 对于从百度爬取的加密的url，进行requests.get()时不允许跳转（allow_redirects=False）
    def original_urls(self):
        tmp_urls = self.baidu_urls  # 暂时的？
        info = []  # 原始的url容器
        for item in tmp_urls: # 遍历列表，tmpurl是一个个元祖,(optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed,Set to True if full redirects are allowed (e.g. re-POST-ing of data at new Location)
            # import ipdb; ipdb.set_trace()  # 不设置为False，结果将是200，设置为True，结果是200
            tmp_page = requests.get(item[0], allow_redirects=False)  # 取出元祖的第一个元素，即网址,allow_redirects重定向，官方API默认为false
            if tmp_page.status_code == 200:
                url_match = re.search(r'\'(.*?)\'', tmp_page.text.encode('utf-8'), re.S)  # 在Python的正则表达式中，有一个参数为re.S。它表示“.”（不包含外侧双引号，下同）的作用扩展到整个字符串，包括“\n”
                info.append((url_match.group(1), item[1]))
            elif tmp_page.status_code == 302:
                info.append((tmp_page.headers.get('location'), item[1]))
            else:
                print 'No URL found!!'
        return info

search_content = raw_input("search target:").decode(sys.stdin.encoding)
print search_content


search = BaiduSearchSpider(search_content)  # 对类实例化
original = search.original_urls  # 调用方法
print '=======Original URLs========'
print original
print '============================'

