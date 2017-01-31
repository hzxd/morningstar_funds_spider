# -*- coding:utf-8 -*-

import requests
import spider
import csv
import parse

def get_info_by_url(url):
    f_fund = open('fund.csv', 'a+')
    f_manager = open('manager.csv', 'a+')
    f_error = open('error.txt', 'a+')
    f_exception = open('exception.txt', 'a+')
    fund_wr = csv.writer(f_fund, quoting=csv.QUOTE_ALL)
    manager_wr = csv.writer(f_manager, quoting=csv.QUOTE_ALL)
    try:
        html = spider.get_root_html(url)
        fund_name = parse.get_fund_name(html)
        fund_id = parse.get_fund_id(html)
        urls = spider.get_urls(html)
        print 'Get urls success'

        fund_html = spider.get_json(requests.get('http://' + urls[1]).content)
        fund = spider.get_fund_info(fund_html)
        print 'Get fund info success'

        manger_html = spider.get_json(requests.get('http://' + urls[0]).content)
        manager = spider.get_manager_info(manger_html)
        print 'Get managers success'

        print 'Get all success'
        for m in manager:
            manager_wr.writerow([fund_id] + [v for v in m.values()])
        fund_wr.writerow([fund_id, fund_name] + [v for v in fund.values()])
    except Exception as e:
        if e.args[0] == 'PageError':
            print 'Page error, writing to the error list'
            f_error.write(url)

        if e.args[0] == 'ParseError':
            print 'Parsing error, writing to the exception list'
            f_exception.write(url)

        print 'Parsing exception, writing to the exception list'
        f_exception.write(url)
    finally:
        f_exception.close()
        f_error.close()
        f_fund.close()
        f_manager.close()


if __name__ == '__main__':
    f = open('urls.txt')

    i = 0
    for u in f.readlines():
        if i<0:
            i+=1
            continue
        get_info_by_url(u)
        i+=1
        print 'Starting get url: {0}, No.{1}'.format(u,i)


    f.close()