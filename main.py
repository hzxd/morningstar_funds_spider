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
        return True
    except Exception as e:
        if len(e.args)>0:
            case = e.args[0]
            switch = {
                'PageError': f_error.write,
                'ParseError':f_exception.write,
            }
            switch.get(case,f_exception.write)(url)
        else:
            f_exception.write(url)
        return False

    finally:
        f_exception.close()
        f_error.close()
        f_fund.close()
        f_manager.close()


if __name__ == '__main__':
    f = open('fund_info.txt')

    i = 0
    for u in f.readlines():
        if i<0:
            i+=1
            continue
        info  = u.split('|')
        for t in info[1:]:
            if len(t)>0:
                print 'try '+t
                url_ = 'http://financials.morningstar.com/fund/management.html?t={t}&region=usa&culture=en_US'.format(t=t)
                if get_info_by_url(url_):
                    break
        i+=1
        print 'Starting get url: {0}, No.{1}'.format(u,i)


    f.close()