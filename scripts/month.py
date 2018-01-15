# scripts/month.py
#
# Usage:
# python manage.py runscript month --script-args arg_code arg_action

from decimal import Decimal

from index.models import Index, Day, Month

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

    # get date(year-month) list
    ym_list = day_list.dates('date', 'month')

    # month list
    month_list = []
    # track
    for ym in ym_list:
        # subset day_list
        days = day_list.filter(date__year=ym.year, date__month=ym.month)
        base = days.first().base
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

    # print list
    print_list(month_list, index)

    # insert
    if arg_action == 'insert':
        insert_list(month_list, index)


def print_list(month_list, index):
    # index
    print("index: {0}".format(index))

    # list
    for i, m in enumerate(month_list):
        print("{0} => {1} | {2} | {3} | {4} = {5}%".format(m['date'], \
            m['open'], m['high'], m['low'] , m['close'], m['change']))
    return


def insert_list(month_list, index):
    # table insert
    for m in month_list:
        index.month_set.create(\
            date=m['date'], \
            open=m['open'], \
            high=m['high'], \
            low=m['low'], \
            close=m['close'], \
            change=m['change'])
    print("\ninsert success\n")
    return

