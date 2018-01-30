# scripts/stock_month.py
#
# Usage:
# python manage.py runscript stock_month --script-args arg_name arg_action

import decimal
from decimal import Decimal

from stock.models import Stock, Day, Month

def run(*args):
    # check argumnet
    if not args:
        print("missing argumnet: name")
        return

    # assign args
    args_len = len(args)
    arg_action = 'none'

    if args_len >= 1:
        arg_name = args[0]
    if args_len >= 2:
        arg_action = args[1]

    # get stock
    stock = Stock.objects.filter(name=arg_name).first()
    if not stock:
        print("no stock")
        return
    print("{name} : {code}".format(name=stock.name, code=stock.code))

    # get day list
    day_list = Day.objects.filter(stock=stock)
    if not day_list:
        print("no data")
        return

    # get month list
    month_list = get_month_list(day_list)
    if not month_list:
        print("no data")
        return

    # print list
    print_list(month_list)

    # insert
    if arg_action == 'insert':
        insert_list(month_list, stock)
    return


def get_month_list(day_list):
    # month list
    month_list = []
    print("Month Tracking : 1...", end='', flush=True)

    # get date(year-month) list
    ym_list = day_list.dates('date', 'month')

    # track
    for ym in ym_list:
        # subset day_list
        days = day_list.filter(date__year=ym.year, date__month=ym.month)
        base = days.first().close - days.first().diff
        # month
        month = {}
        month['date'] = ym
        month['open'] = days.first().open
        month['high'] = days.order_by('-high').first().high
        month['low'] = days.order_by('-low').last().low
        month['close'] = days.last().close
        month['change'] = round((month['close'] - base) / base * 100, 2)
        # append
        month_list.append(month)
    # count month
    print("{0}".format(len(month_list)))
    return month_list


def print_list(month_list):
    # list
    print("")
    for v in month_list[:5]:
        print("{0} => {1} | {2} | {3} | {4} = {5}%".format(v['date'], \
            v['open'], v['high'], v['low'] , v['close'], v['change']))
    print("")
    for v in month_list[-5:]:
        print("{0} => {1} | {2} | {3} | {4} = {5}%".format(v['date'], \
            v['open'], v['high'], v['low'] , v['close'], v['change']))
    print("")
    return


def insert_list(month_list, stock):
    # table insert
    print("insert :", end=' ', flush=True)
    for v in month_list:
        stock.month_set.create(\
            date=v['date'], \
            open=v['open'], \
            high=v['high'], \
            low=v['low'], \
            close=v['close'], \
            change=v['change'])
    print("success\n")
    return

