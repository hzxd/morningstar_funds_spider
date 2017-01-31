# -*- coding:utf-8 -*-
import json
import requests
import re
import parse
MANGER_FIELDS = [
    'manager_name',
    'manager_time',
    'manager_abstract',
    'manager_certification',
    'manager_education',
]
ADVISOR_FIELDS = [
    'fund_inception',
    'fund_subadvisor',
    'fund_name_of_issuer',
    'fund_advisor',
]



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


def get_root_html(url):
    req = requests.get(url)
    if req.content.find('Error Page') > 0 or req.content.find('script') < 0:
        raise Exception("PageError")
    return req.content


def get_fund_info(html):
    result = {}
    for field in ADVISOR_FIELDS:
        print 'Get ' + field
        result[field] = getattr(parse, 'get_' + field)(html).encode('utf-8')
    return result


def get_manager_info(html):
    html = parse.check_bs4(html)
    tr_htmls = html.find('tbody').children
    result = []
    for tr_html in tr_htmls:
        if tr_html.name !='tr':
            continue
        if tr_html.attrs.get('class', None) is not None and \
                len(tr_html.attrs['class'])>0:
            continue

        manager = {}
        for field in MANGER_FIELDS:
            print 'Get '+field
            manager[field] = getattr(parse, 'get_' + field)(tr_html).encode('utf-8')
        result.append(manager)
    return result

# def get_manager_info(url):
#     try:
#
#     except Exception, e:
#         print e.args
#         return None
#     result = list()
#     result.append(parse.get_fund_name(html).encode('utf-8'))
#     result.append(parse.get_fund_name(html).encode('utf-8'))
#     for field in manger_fields:
#         result.append(getattr(parse, 'get_' + field)(manger_html).encode('utf-8'))
#     for field in advisor_fields:
#         result.append(getattr(parse, 'get_' + field)(advisor_html).encode('utf-8'))
#
#     return result
