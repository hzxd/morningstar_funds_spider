# -*- coding:utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
import parse
import re
import spider


if __name__ == '__main__':
    f = open('urls.txt')
    f_result = open('result.csv','a+')
    f_error = open('error.csv','a+')
    for url in f.readlines():
        print '开始抓取{0}'.format(url)

        html = spider.get_root_html(url)

        urls = spider.get_urls()
        if not r:
            print '抓取失败, 写入失败列表'
            f_error.write(url)
        else:
            print r
            print '抓取成功, 写入结果集'
            f_result.write('\t'.join(r)+'\n')
