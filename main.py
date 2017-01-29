# -*- coding:utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
import parse
import re


def get_json(text):
    json_dict = json.loads(text)
    html = json_dict['html']
    return html


def get_manager_url(text):
    url = re.search('(financials.*c-managers\.action.*callback=)', text)
    return url.group(0)


def get_advisorinfo_url(text):
    url = re.search('(financials.*c-advisorInfo\.action.*callback=)', text)
    return url.group(0)


def get_urls(html):
    manager_url = get_manager_url(html)
    advisor_url = get_advisorinfo_url(html)
    return manager_url, advisor_url


def get_fund_info(url):
    req = requests.get(url)
    if req.content.find('Error Page')>0 or req.content.find('script') < 0:
        return None
    html = req.content
    urls = get_urls(html)

    manger_fields = [
        'manager_name',
        'manager_time',
        'manager_abstract',
        'manager_certification',
        'manager_education',
    ]
    advisor_fields = [
        'fund_inception',
        'fund_subadvisor',
        'fund_name_of_issuer',
        'fund_advisor',
    ]
    try:
        manger_html = get_json(requests.get('http://' + urls[0]).content)
        advisor_html = get_json(requests.get('http://' + urls[1]).content)
    except Exception,e:
        print e.args
        return None
    result = list()
    result.append(parse.get_fund_name(html).encode('utf-8'))
    result.append(parse.get_fund_name(html).encode('utf-8'))
    for field in manger_fields:
        result.append(getattr(parse, 'get_' + field)(manger_html).encode('utf-8'))
    for field in advisor_fields:
        result.append(getattr(parse, 'get_' + field)(advisor_html).encode('utf-8'))

    return result

if __name__ == '__main__':
    f = open('urls.txt')
    f_result = open('result.csv','a+')
    f_error = open('error.csv','a+')
    for url in f.readlines():
        print '开始抓取{0}'.format(url)
        r = get_fund_info(url)
        if not r:
            print '抓取失败, 写入失败列表'
            f_error.write(url)
        else:
            print r
            print '抓取成功, 写入结果集'
            f_result.write('\t'.join(r)+'\n')
