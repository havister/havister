# scripts/index_day_update.py
#
# index_day 테이블에서 change를 업데이트 한다.
#
# Usage:
# python manage.py runscript index_day_update --script-args arg_code arg_action

from decimal import Decimal, getcontext, ROUND_HALF_UP

from index.models import Index, Day

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
        print("no code")
        return
    print("{name} : {code}".format(name=index.name, code=index.code))

    # get day list
    day_list = Day.objects.filter(index=index)
    if not day_list:
        print("no data")
        return

    # tracking
    for day in day_list:
        base = day.close - day.diff
        new_change = round(day.diff / base * 100, 2)
        # update
        if day.change == new_change:
            continue
        print("{0} : {1}% => {2}%".format(day.date, day.change, new_change), end=' ', flush=True)
        if arg_action == 'update':
            day.change = new_change
            day.save()
            print(": updated")
        else:
            print("")
    return

