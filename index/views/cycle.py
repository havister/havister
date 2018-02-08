"""havister index views
"""
import decimal
from dateutil.relativedelta import relativedelta

from django.views import generic

from index.models import Index, Day, Cycle

class CycleView(generic.DetailView):
    model = Index
    context_object_name = 'index'
    template_name = 'index/cycle.html'

    def __init__(self):
        dc = decimal.getcontext()
        dc.prec = 9
        dc.rounding = decimal.ROUND_HALF_UP

    def get_context_data(self, **kwargs):
        # base 
        context = super(CycleView, self).get_context_data(**kwargs)
        # index object
        index = kwargs['object']
        # cycle list
        context['detail_list'] = self.get_detail_list(index)
        # alpha list
        if context['detail_list']:
            context['alpha_list'] = self.get_alpha_list(context['detail_list'])
        return context

    def get_detail_list(self, index):
        cycle_list = list(Cycle.objects.filter(index=index))
        if not cycle_list:
            return
        last = cycle_list[-1]
        today = Day.objects.filter(index=index).last()

        if today.date > last.date:
            # today
            if today.close != last.close:
                change = round((today.close - last.close) / last.close * 100, 2)
            else:
                change = Decimal('0.00')
            # cycle
            cycle = Cycle(date=today.date, close=today.close, change=change, certainty=False, index=index)
            # cycle list
            cycle_list.append(cycle)
        return cycle_list

    def get_alpha_list(self, cycle_list):
        base_date = cycle_list[0].date
        close_date = base_date
        alpha_list = []

        for cycle in cycle_list[1:]:
            # range
            base_date = close_date
            close_date = cycle.date
            period = relativedelta(close_date, base_date)
            delta = ""
            if period.years:
                years = "{0}년".format(period.years)
                delta = years
            if period.months:
                if delta:
                    delta += ", "
                months = "{0}월".format(period.months)
                delta += months
            if period.days:
                if delta:
                    delta += ", "
                days = "{0}일".format(period.days)
                delta += days
            # alpha
            alpha = {}
            alpha['base_date'] = base_date
            alpha['close_date'] = close_date
            alpha['period'] = delta
            alpha['close'] = cycle.close
            alpha['change'] = cycle.change 
            alpha['certainty'] = cycle.certainty 
            # alpha list
            alpha_list.append(alpha)
        return alpha_list

