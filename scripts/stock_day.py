# scripts/stock_day.py
#
# Usage:
# python manage.py runscript stock_day --script-args arg_name, arg_base_date, arg_action

import requests
from bs4 import BeautifulSoup

from stock.models import Stock, Day

def run(*args):
    # check argumnet
    if not args:
        print("missing argumnet: name")
        return

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
        soup = BeautifulSoup(html, "lxml")
        table = soup.table

        # [0]date, [1]close, [2]diff, [3]open, [4]high, [5]low
        for tr in table.find_all('tr'):
            day = {}
            spans = tr.find_all('span')
            if not spans:
                continue
            # date
            day['date'] = spans[0].string.strip().replace('.', '-')
            if day['date'] < base_date or \
                (len(day_list) and day['date'] >= day_list[-1]['date']): # 마지막 페이지를 넘었을 경우
                print("{page}".format(page=page))
                page = -1
                break
            if day['date'] >= '2018-01-01':
                continue
            # OHLC
            day['open'] = int(spans[3].string.strip().replace(',',''))
            day['high'] = int(spans[4].string.strip().replace(',',''))
            day['low'] = int(spans[5].string.strip().replace(',',''))
            day['close'] = int(spans[1].string.strip().replace(',',''))
            # diff
            diff = int(spans[2].string.strip().replace(',',''))
            if diff and spans[2]['class'][-1].find('nv') != -1: # 하락(음수) 확인
                diff = diff * -1
            if diff == day['open'] or diff == day['close']: # 데이터 오류 보정
                diff = 0
            day['diff'] = diff
            # change
            base = day['close'] - day['diff']
            day['change'] = round(day['diff'] / base * 100, 2)

            # day_list
            day_list.append(day)

    # base diff to zero 
    if day_list[-1]['diff']:
        day_list[-1]['diff'] = 0
        day_list[-1]['change'] = 0.0
    # sort by date
    day_list.reverse()
    return day_list


def get_page_url(code, page):
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'.\
        format(code=code, page=page)
    return url


def get_html(url):
    html = ""
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
    return html


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

