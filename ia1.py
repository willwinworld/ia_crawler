# -*- coding: utf-8 -*-


import re
import requests
from pyquery import PyQuery as pq
import sys


class BaiduSearchSpider(object):

    def __init__(self, search_text):
        self.url = "http://www.baidu.com/baidu?wd=%s" % search_text
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"}
        self._page = None
    
    @property
    def page(self):
        if not self._page:
            r = requests.get(self.url, headers=self.headers)
            r.encoding = 'utf-8'
            self._page = pq(r.text)
        return self._page
    
    @property
    def baidu_urls(self):
        return [(site.attr('href'), site.text().encode('utf-8')) for site in self.page('div.result.c-container h3.t a').items()]
    
    @property
    def original_urls(self):
        tmp_urls = self.baidu_urls
        info = []
        for item in tmp_urls:
            tmp_page = requests.get(item[0], allow_redirects=False)
            if tmp_page.status_code == 200:
                url_match = re.search(r'\'(.*?)\'', tmp_page.text.encode('utf-8'), re.S)
                info.append((url_match.group(1), item[1]))
            elif tmp_page.status_code == 302:
                info.append((tmp_page.headers.get('location'), item[1]))
            else:
                print 'No URL found!!'
        return info

search_content = raw_input("search target:").decode(sys.stdin.encoding)
print search_content


search = BaiduSearchSpider(search_content)
original = search.original_urls
print '=======Result========'
print original
print '====================='

