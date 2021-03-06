# scripts/index_cycle.py
#
# index_day 테이블에서 일별 데이터를 집계하여 순환별 데이터를 생성
#
# Usage:
# python manage.py runscript index_cycle --script-args arg_code arg_action

from decimal import Decimal, getcontext, ROUND_HALF_UP

from index.models import Index, Day, Cycle

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

    # get cycle list
    cycle_list = get_cycle_list(day_list)
    if not cycle_list:
        print("no data")
        return

    # print list 
    print_list(cycle_list)

    # insert
    if arg_action == 'insert':
        insert_list(cycle_list, index)
    return


def get_cycle_list(day_list):
    # cycle list
    cycle_list = []
    print("Cycle Tracking : 1...", end='', flush=True)

    # base day
    check = day_list[0]
    list_append(cycle_list, check)
    top = check.close

    # reversal rate 30%
    RATE = Decimal('0.3')

    # track
    track = {}
    track['top'] = check.close - check.diff
    track['brick'] = round(track['top'] * RATE, 2)
    track['bot'] = Decimal(0)

    # track
    for day in day_list[1:]:
        date = day.date
        close = day.close

        # 상승 모드인가?
        if track['top']:
            # 신규 고점인가?
            if close > track['top']:
                # 고점 리셋
                track['top'] = close
                track['brick'] = round(track['top'] * RATE, 2)
                check = day

            # 하락 전환인가?
            elif close <= track['top'] - track['brick']:
                # 고점 기록
                top = track['top']
                # 전환 추가
                list_append(cycle_list, check)
                check = day
                # 모드 전환
                track['bot'] = close
                track['top'] = Decimal(0)

        # 하락 모드인가?
        elif track['bot']:
            # 신규 저점인가?
            if close < track['bot']:
                # 저점 리셋
                track['bot'] = close
                check = day

            # 전 고점 회복인가?
            elif close >= top:
                # 전환 추가
                list_append(cycle_list, check)
                check = day
                # 모드 전환
                track['top'] = close
                track['brick'] = round(track['top'] * RATE, 2)
                track['bot'] = Decimal(0)
        # endif
    # endfor
    else:
        list_append(cycle_list, check)
        cycle_list[-1]['certainty'] = False

    # count cycle
    print("{0}".format(len(cycle_list)))
    return cycle_list


def list_append(cycle_list, day):
    # base, close
    if not cycle_list:
        base = day.close
        close = day.close
    else:
        base = cycle_list[-1]['close']
        close = day.close
        # check duplication
        last_date = cycle_list[-1]['date']
        if last_date == day.date:
            return
    # change
    change = round((close - base) / base * 100, 2)
    # cycle
    cycle = {'date': day.date, 'close':day.close, 'change': change, 'certainty': True}
    # cycle list
    cycle_list.append(cycle)
    return


def print_list(cycle_list):
    # list
    print("")
    for v in cycle_list:
        print("{0} : {1} ({2}%) : {3}".format(v['date'], v['close'], v['change'], v['certainty']))
    print("")
    return


def insert_list(cycle_list, index):
    # table insert
    print("insert :", end=' ', flush=True)
    for cycle in cycle_list:
        index.cycle_set.create(date=cycle['date'], \
            close=cycle['close'], \
            change=cycle['change'], \
            certainty=cycle['certainty'])
    print("success\n")
    return

