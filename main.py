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


url = 'http://financials.morningstar.com/fund/management.html?t=MRLSX&region=usa&culture=en_US'
req = requests.get(url)
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
manger_html = get_json(requests.get('http://' + urls[0]).content)
advisor_html = get_json(requests.get('http://' + urls[1]).content)
result = {}
for field in manger_fields:
    result[field] = getattr(parse, 'get_' + field)(manger_html)
for field in advisor_fields:
    result[field] = getattr(parse, 'get_' + field)(advisor_html)

result['fund_name'] = parse.get_fund_name(html)
result['fund_id'] = parse.get_fund_name(html)
print result
