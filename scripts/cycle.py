# scripts/cycle.py
#
# Usage:
# python manage.py runscript cycle --script-args arg_code arg_action

from decimal import Decimal

from index.models import Index, Day, Cycle

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
    # make cycle list
    #
    cycle_list = []
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
                    list_append(cycle_list, check)
                    direction = 1
                check = day

        # 전환 크기 이하인가?
        elif close <= track['h'] - track['hs']:
            # 상승중 이었나?
            if direction > 0:
                list_append(cycle_list, check)
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
        list_append(cycle_list, check)
        cycle_list[-1]['fix'] = False

    # report 
    print_list(cycle_list, day, item)

    # insert
    if arg_action == 'insert':
        insert_list(cycle_list, item)


def list_append(cycle_list, day):
    # base
    if cycle_list:
        # check date duplication
        if cycle_list[-1]['date'] == day.date:
            return
        # last close
        else:
            base = cycle_list[-1]['close']
    else:
        # initialize
        base = day.base
    # diff
    diff = day.close - base
    change = round(diff / base * 100, 2)

    # cycle
    cycle = {'date': day.date, 'base': base, 'close':day.close, 'diff': diff, 'change': change, 'fix': True}
    # cycle list
    cycle_list.append(cycle)
    return


def print_list(cycle_list, today, item):
    # index item
    print("{0}".format(item))

    # list
    for cycle in cycle_list:
        print("{0} {1} => {2} = {3}({4}%) : {5}".format(cycle['date'], cycle['base'], cycle['close'], cycle['diff'], cycle['change'], cycle['fix']))
    return


def insert_list(cycle_list, item):
    # table insert
    for cycle in cycle_list:
        item.cycle_set.create(date=cycle['date'], \
            base=cycle['base'], \
            close=cycle['close'], \
            diff=cycle['diff'], \
            change=cycle['change'], \
            fix=cycle['fix'])
    print("\ninsert success\n")
    return

