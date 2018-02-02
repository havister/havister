# scripts/index_month.py
#
# index_day 테이블에서 일별 데이터를 집계하여 월별 데이터를 생성
#
# Usage:
# python manage.py runscript index_month --script-args arg_code arg_action

import calendar
from decimal import Decimal, getcontext, ROUND_HALF_UP

from index.models import Index, Day, Month

def run(*args):
    # check argumnet
    if not args:
        print("missing argumnet: code")
        return

    # 실수 연산 반올림 보정
    context = getcontext()
    context.prec = 9
    context.rounding = ROUND_HALF_UP

    # assign args
    args_len = len(args)
    arg_action = 'none'

    if args_len >= 1:
        arg_code = args[0]
    if args_len >= 2:
        arg_action = args[1]

    # get index
    index = Index.objects.filter(code=arg_code).first()
    if not index:
        print("no index")
        return
    print("{name} : {code}".format(name=index.name, code=index.code))

    # get day list
    day_list = Day.objects.filter(index=index)
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
        insert_list(month_list, index)
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
        month['date'] = get_last_day(ym.year, ym.month)
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


def get_last_day(year, month):
    day = calendar.monthrange(year, month)[1]
    last_day = "{0}-{1:02}-{2}".format(year, month, day)
    return last_day


def print_list(month_list):
    # list
    print("")
    for v in month_list[:5]:
        print("{0} : {1} | {2} | {3} | {4} = {5}%".format(v['date'], \
            v['open'], v['high'], v['low'] , v['close'], v['change']))
    print("")
    for v in month_list[-5:]:
        print("{0} : {1} | {2} | {3} | {4} = {5}%".format(v['date'], \
            v['open'], v['high'], v['low'] , v['close'], v['change']))
    print("")
    return


def insert_list(month_list, index):
    # table insert
    print("insert :", end=' ', flush=True)
    for v in month_list:
        index.month_set.create(\
            date=v['date'], \
            open=v['open'], \
            high=v['high'], \
            low=v['low'], \
            close=v['close'], \
            change=v['change'])
    print("success\n")
    return

