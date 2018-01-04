# scripts/insert_reversal.py
#
# Usage:
# python manage.py runscript delete_all_questions --script-args arg_code arg_action

from decimal import Decimal
from index.models import Index, Day, Reversal

def run(*args):
    # check argumnet
    if not args:
        print("missing argumnet: code")
        return
    else:
        arg_code = args[0]
    if len(args) >= 2:
        arg_action = args[1]
    else:
        arg_action = 'none'

    # get index object 
    item = Index.objects.filter(code=arg_code).first()
    if not item:    
        print("no code: '{0}'".format(arg_code))
        return

    # get day list
    exists = Day.objects.filter(index=item).exists()
    if not exists:
        print("empty data")
        return
    day_list = Day.objects.filter(index=item)

    #
    # make reversal list
    #
    reversal_list = []
    # reveral rate 30%
    RATE = Decimal('0.3')
    # base day
    check = day_list[0]
    # base direction (1: up, 2: down)
    direction = 1;

    # initialize track
    track = {}
    track['h'] = check.base
    track['l'] = check.base
    track['hs'] = round(track['h'] * RATE, 2)
    track['ls'] = round(track['l'] * RATE, 2)

    # track
    for day in day_list:
        date = day.date
        close = day.close

        # 신규 고점인가?
        if close > track['h']:
            track['h'] = close
            track['hs'] = round(track['h'] * RATE, 2)
            # 전환 크기 이상인가?
            if close >= track['l'] + track['ls']:
                # 하락중 이었나?
                if direction < 0:
                    list_append(reversal_list, check)
                    direction = 1
                check = day

        # 전환 크기 이하인가?
        elif close <= track['h'] - track['hs']:
            # 상승중 이었나?
            if direction > 0:
                list_append(reversal_list, check)
                direction = -1
                # 저점 리셋 
                track['l'] = close
                track['ls'] = round(track['l'] * RATE, 2)
                check = day

            # 신규 저점인가?
            elif close < track['l']:
                track['l'] = close
                track['ls'] = round(track['l'] * RATE, 2)
                check = day
        # endif
    # endfor
    else:
        list_append(reversal_list, check)

    # report 
    print_list(reversal_list, day, item)

    # insert
    if arg_action == 'insert':
        insert_list(reversal_list, item)


def list_append(reversal_list, day):
    # base
    if reversal_list:
        # check duplication
        if reversal_list[-1]['date'] == day.date:
            return
        base = reversal_list[-1]['close']
    else:
        base = day.base
    # difference
    difference = day.close - base
    change = round(difference / base * 100, 2)

    # reversal
    reversal = {'date': day.date, 'base': base, 'close':day.close, 'difference': difference, 'change': change}
    # reversal list
    reversal_list.append(reversal)
    return


def print_list(reversal_list, today, item):
    # index item
    print("{0}".format(item))

    # list
    for reversal in reversal_list:
        print("{0} {1} => {2} = {3}({4}%)".format(reversal['date'], reversal['base'], reversal['close'], reversal['difference'], reversal['change']))

    # with today
    pre_close = reversal['close']
    if today.close > pre_close:
        change = round((today.close - pre_close) / pre_close * 100, 2)
    elif today.close < pre_close:
        change = round((pre_close - today.close) / pre_close * -100, 2)
    else:
        change = Decimal('0.0')
    print("{0} {1} => {2} = {3}({4}%)".format(today.date, pre_close, today.close, today.close - pre_close, change))
    return


def insert_list(reversal_list, item):
    # table insert
    for reversal in reversal_list:
        item.reversal_set.create(date=reversal['date'], \
            base=reversal['base'], \
            close=reversal['close'], \
            difference=reversal['difference'], \
            change=reversal['change'])
    print("\ninsert success\n")
    return

