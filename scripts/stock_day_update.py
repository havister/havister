# scripts/stock_day_update.py
#
# stock_day 테이블에서 diff를 업데이트 한다.
#
# Usage:
# python manage.py runscript stock_day_update --script-args arg_name arg_action

from stock.models import Stock, Day

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

    # get stock_list
    stock_list = []
    if arg_name == 'all:future':
        stock_list = Stock.objects.filter(future=True)
    elif arg_name == 'all:option':
        stock_list = Stock.objects.filter(option=True)
    else:
        stock_list = Stock.objects.filter(name=arg_name)
    if not stock_list:
        print("no stock\n")
        return

    # iterate stock_list
    for i, stock in enumerate(stock_list):
        print("{no}) {name} : {code}".format(no=i+1, name=stock.name, code=stock.code))
        print("tracking...", end=' ', flush=True)

        # get day list
        day_list = Day.objects.filter(stock=stock)
        if not day_list:
            print("no data : day\n")
            return

        # tracking
        base = day_list[0].close
        for day in day_list:
            # diff
            day.diff = day.close - base
            base = day.close
            # update
            if arg_action == 'update':
                day.save()

        # report
        if arg_action == 'update':
            print("updated\n")
        else:
            print("done\n")
    return

