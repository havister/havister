# scripts/expiration.py
#
# Usage:
# python manage.py runscript expiration --script-args arg_code arg_action

from decimal import Decimal

from expiration.models import Period 
from index.models import Index, Day, Expiration

def run(*args):
    # check argumnet
    if not args:
        print("missing argumnet: code")
        return
    # assign args
    args_len = len(args)
    if args_len >= 1:
        arg_code = args[0]
    if args_len >= 2:
        arg_action = args[1]
    else:
        arg_action = 'none'

    # get index
    index = Index.objects.filter(code=arg_code).first()
    if not index:
        print("no code")
        return

    # get day list
    day_list = Day.objects.filter(index=index)
    if not day_list:
        print("no data")
        return

    # get expiration period
    period_list = Period.objects.all()
    if not period_list:
        print("no period")
        return

    # expiration list
    expiration_list = []
    # track
    for period in period_list:
        month = period.month
        open_date = period.open_date
        close_date = period.close_date
        # expiration
        expiration = {}
        days = day_list.filter(date__range=(open_date, close_date))
        expiration['date'] = close_date
        expiration['base'] = days.first().base
        expiration['open'] = days.first().open
        expiration['high'] = days.order_by('-high').first().high
        expiration['low'] = days.order_by('-low').last().low
        expiration['close'] = days.last().close
        expiration['diff'] = expiration['close'] - expiration['base']
        expiration['change'] = round(expiration['diff'] / expiration['base'] * 100, 2)
        # append
        expiration_list.append(expiration)

    # print list
    print_list(expiration_list, index)

    # insert
    if arg_action == 'insert':
        insert_list(expiration_list, index)


def print_list(expiration_list, index):
    # index
    print("index: {0}".format(index))

    # list
    for e in expiration_list:
        print("{0} {1} => {2} | {3} | {4} | {5} = {6} ({7}%)".format(e['date'], e['base'], \
            e['open'], e['high'], e['low'] , e['close'], e['diff'], e['change']))
    return


def insert_list(expiration_list, index):
    # table insert
    for e in expiration_list:
        index.expiration_set.create(\
            date=e['date'], \
            base=e['base'], \
            open=e['open'], \
            high=e['high'], \
            low=e['low'], \
            close=e['close'], \
            diff=e['diff'], \
            change=e['change'])
    print("\ninsert success\n")
    return
