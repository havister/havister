# scripts/stock_expiration.py
#
# stock_day 테이블에서 일별 데이터를 집계하여 만기별 데이터를 생성
#
# Usage:
# python manage.py runscript stock_expiration --script-args arg_name arg_action

from decimal import Decimal, getcontext, ROUND_HALF_UP

from expiration.models import Period 
from stock.models import Stock, Day, Expiration

def run(*args):
    # check argumnet
    if not args:
        print("missing argumnet: name")
        return

    # 실수 연산 반올림 보정
    context = getcontext()
    context.prec = 9
    context.rounding = ROUND_HALF_UP

    # assign args
    args_len = len(args)
    arg_action = 'none'

    if args_len >= 1:
        arg_name = args[0]
    if args_len >= 2:
        arg_action = args[1]

    # get expiration period
    period_list = Period.objects.all()
    if not period_list:
        print("no period")
        return

    # get stock_list
    stock_list = []
    if arg_name == 'all:option':
        stock_list = Stock.objects.filter(option=True)
    else:
        stock_list = Stock.objects.filter(name=arg_name, option=True)
    if not stock_list:
        print("no stock\n")
        return

    # iterate stock_list
    for i, stock in enumerate(stock_list):
        print("{no}) {name} : {code}".format(no=i+1, name=stock.name, code=stock.code))

        # get day list
        day_list = Day.objects.filter(stock=stock)
        if not day_list:
            print("no data : day\n")
            continue

        # get expiration list
        expiration_list = get_expiration_list(day_list, period_list)
        if not expiration_list:
            print("no data : expiration\n")
            continue

        # print list
        print_list(expiration_list)

        # insert
        if arg_action == 'insert':
            insert_list(expiration_list, stock)
    return


def get_expiration_list(day_list, period_list):
    # expiration list
    expiration_list = []
    print("Expiration Tracking : 1...", end='', flush=True)

    # track
    for period in period_list:
        month = period.month
        open_date = period.open_date
        close_date = period.close_date
        # check date
        if not day_list.filter(date__gte=close_date).first():
            break;
        # subset day_list
        days = day_list.filter(date__range=(open_date, close_date))
        if not days:
            continue
        base = days.first().close - days.first().diff
        # expiration
        expiration = {}
        expiration['date'] = close_date
        expiration['open'] = days.first().open
        expiration['high'] = days.order_by('-high').first().high
        expiration['low'] = days.order_by('-low').last().low
        expiration['close'] = days.last().close
        expiration['change'] = round(Decimal(str((expiration['close'] - base) / base)) * 100, 2)
        # append
        expiration_list.append(expiration)
    # count expiration
    print("{0}".format(len(expiration_list)))
    return expiration_list


def print_list(expiration_list):
    # list
    print("")
    for v in expiration_list[:5]:
        print("{0} : {1} | {2} | {3} | {4} = {5}%".format(v['date'], \
            v['open'], v['high'], v['low'] , v['close'], v['change']))
    print("")
    for v in expiration_list[-5:]:
        print("{0} : {1} | {2} | {3} | {4} = {5}%".format(v['date'], \
            v['open'], v['high'], v['low'] , v['close'], v['change']))
    print("")
    return


def insert_list(expiration_list, stock):
    # table insert
    print("insert :", end=' ', flush=True)
    for v in expiration_list:
        stock.expiration_set.create(\
            date=v['date'], \
            open=v['open'], \
            high=v['high'], \
            low=v['low'], \
            close=v['close'], \
            change=v['change'])
    print("success\n")
    return

