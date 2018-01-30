# scripts/index_day_update.py
#
# Usage:
# python manage.py runscript index_day_update --script-args arg_code

from decimal import Decimal

from index.models import Index, Day

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

    # track
    for day in day_list:
        base = day.close - day.diff
        day.change = round(day.diff / base * 100, 2)
        day.save()
        print(day)
    return

