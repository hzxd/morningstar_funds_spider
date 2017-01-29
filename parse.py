# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import string
import re

M_DASH = u'—'


def check_bs4(text):
    if not isinstance(text, BeautifulSoup):
        text = strip(text)
        text = BeautifulSoup(text, 'lxml')
    return text


def strip(text):
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    text = string.strip(text)
    return text


def get_manager_name(tr_text):
    tr_text = check_bs4(tr_text)
    return strip(tr_text.th.contents[0])


def get_manager_time(tr_text):
    tr_text = check_bs4(tr_text)
    time = tr_text.th.span.text
    time = strip(time)
    if time.find(M_DASH) == -1:
        return ''
    else:
        return '-'.join([strip(t) for t in time.split(M_DASH)])


def get_manager_abstract(tr_text):
    tr_text = check_bs4(tr_text)
    return tr_text.td.table.tr.td.get_text()


def get_manager_certification(tr_text):
    tr_text = check_bs4(tr_text)
    td = tr_text.find(text='Certification')
    if not td:
        return ''
    return td.parent.parent.next_sibling.next_sibling.get_text()


def get_manager_education(tr_text):
    tr_text = check_bs4(tr_text)
    schools = tr_text.find(text='Education').parent.parent.next_sibling.next_sibling
    return '\n'.join([strip(i.get_text().replace(u',', '')) for i in schools.find_all('td')])


def get_info_by_key_words(text, key):
    text = check_bs4(text)
    info = text.find(text=re.compile(".*{key}.*".format(key=key)))
    if info is None:
        raise ValueError
    result = info.parent.parent.td.get_text()
    return strip(result)


def get_fund_inception(text):
    return get_info_by_key_words(text, 'Fund Inception')


def get_fund_name_of_issuer(text):
    return get_info_by_key_words(text, 'Name of Issuer')


def get_fund_advisor(text):
    return get_info_by_key_words(text, 'Fund Advisor')


def get_fund_subadvisor(text):
    return get_info_by_key_words(text, 'Subadvisor')


def get_fund_name(text):
    text = check_bs4(text)
    name = text.find(attrs={'class': 'r_title'}).h1
    if not name:
        raise ValueError
    return name.get_text()


def get_fund_id(text):
    text = check_bs4(text)
    name = text.find(attrs={'class': 'r_title'}).h1
    if not name:
        raise ValueError
    return name.get_text()
