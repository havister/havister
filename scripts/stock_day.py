# scripts/stock_day.py
#
# 다음 금융 페이지에서 일별 시세 데이터(수정주가) 가져와 데이터베이스에 저장
# (http://finance.daum.net/item/quote_yyyymmdd_sub.daum?page=1&code=005930&modify=1)
#
# Usage:
# python manage.py runscript stock_day --script-args arg_name, arg_base_date, arg_action

import requests
from bs4 import BeautifulSoup
from decimal import Decimal, getcontext, ROUND_HALF_UP

from stock.models import Stock, Day

def run(*args):
    # check argumnet
    if not args:
        print("missing argumnet: name")
        return

    # 실수 연산 반올림 보정
    getcontext().rounding = ROUND_HALF_UP

    # assign args
    args_len = len(args)
    arg_base_date = '2017-12-01'
    arg_action = 'none'

    if args_len >= 1:
        arg_name = args[0]
    if args_len >= 2:
        arg_base_date = args[1]
    if args_len >= 3:
        arg_action = args[2]

    # get stock
    stock = Stock.objects.filter(name=arg_name).first()
    if not stock:
        print("no stock")
        return
    print("{name} : {code}".format(name=stock.name, code=stock.code))

    # get day list
    day_list = get_day_list(stock.code, arg_base_date)
    if not day_list:
        print("no data")
        return

    # print list
    print_list(day_list)

    # insert
    if arg_action == 'insert':
        insert_list(day_list, stock)
    return


def get_day_list(code, base_date):
    # day list
    day_list = []
    page = 0
    print("Data Page : 1...", end='', flush=True)

    # read data
    while (page >= 0):
        # url
        page += 1;
        page_url = get_page_url(code, page)

        # html
        html = get_html(page_url)
        # table
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table', id='bbsList')

        # [0]date, [1]open, [2]high, [3]low, [4]close
        trs = table.find_all('tr', onmouseout=True)
        if not trs:
            page -= 1
            break;
        for tr in trs:
            if not tr:
                page *= -1
                break
            tds = tr.find_all('td')
            day = {}
            # date
            day['date'] = convert_date_string(tds[0].string.strip())
            if day['date'] < base_date:
                page *= -1
                break
            if day['date'] >= '2018-02-01':
                continue
            # OHLC
            day['open'] = int(tds[1].string.strip().replace(',', ''))
            day['high'] = int(tds[2].string.strip().replace(',', ''))
            day['low'] = int(tds[3].string.strip().replace(',', ''))
            day['close'] = int(tds[4].string.strip().replace(',', ''))
            # day_list
            day_list.append(day)
    # end page
    print("{page}".format(page=abs(page)))
    # sort by date
    day_list.reverse()

    # diff, change
    first_day = day_list[0]
    first_day['diff'] = 0
    first_day['change'] = Decimal('0.00')
    base = first_day['close']

    for day in day_list[1:]:
        # diff
        day['diff'] = day['close'] - base
        # change
        day['change'] = round(Decimal(str(day['diff'] / base)) * 100, 2)
        base = day['close']
    # day_list
    return day_list


def get_page_url(code, page):
    url = 'http://finance.daum.net/item/quote_yyyymmdd_sub.daum?page={page}&code={code}&modify=1'.\
        format(page=page, code=code)
    return url


def get_html(url):
    html = ""
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
    return html


def convert_date_string(yymmdd):
    split = yymmdd.split('.')
    yy = split[0]
    if int(yy) >= 50:
        yyyy = '19' + yy
    else:
        yyyy = '20' + yy
    yyyymmdd = "{0}-{1}-{2}".format(yyyy, split[1], split[2])
    return yyyymmdd


def print_list(day_list):
    # list
    print("")
    for v in day_list[:5]:
        print("{0} : {1} | {2} | {3} | {4} = {5} ({6}%)".format(v['date'], \
            v['open'], v['high'], v['low'] , v['close'], v['diff'], v['change']))
    print("")
    for v in day_list[-5:]:
        print("{0} : {1} | {2} | {3} | {4} = {5} ({6}%)".format(v['date'], \
            v['open'], v['high'], v['low'] , v['close'], v['diff'], v['change']))
    print("")
    return


def insert_list(day_list, stock):
    # table insert
    print("insert :", end=' ', flush=True)
    for v in day_list:
        stock.day_set.create(\
            date=v['date'], \
            open=v['open'], \
            high=v['high'], \
            low=v['low'], \
            close=v['close'], \
            diff=v['diff'], \
            change=v['change'])
    print("success\n")
    return

