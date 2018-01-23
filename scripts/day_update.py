# scripts/day.py
#
# Usage:
# python manage.py runscript day --script-args arg_code

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
        if day.diff:
            continue
        diff = day.close - day.base
        change = round(diff / day.base * 100, 2)
        if change == day.change:
            day.diff = diff
            day.save()
            print(day)
        else:
            print("{0} d:{1} {2} {3}".format(day.date, diff, change, day.change))
            break;
    return

