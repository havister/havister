"""havister index views
"""
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.views import generic

from .models import Index, Day, Month, Cycle, Expiration

class IndexList(generic.ListView):
    context_object_name = 'index_list'
    template_name = 'index/list.html'

    def get_queryset(self):
        return Index.objects.order_by('-market', '-future', '-option', '-fund')


class IndexBasic(generic.DetailView):
    model = Index
    context_object_name = 'index'
    template_name = 'index/basic.html'

    def get_context_data(self, **kwargs):
        # base 
        context = super(IndexBasic, self).get_context_data(**kwargs)
        # index object
        context_index = kwargs['object']
        # month list
        context['month_list'] = Month.objects.filter(index=context_index)
        # summary list 
        if context['month_list']:
            context['summary_list'] = self.get_summary_list(context['month_list'])
        return context

    def get_summary_list(self, month_list):
        years = [1, 3, 5, 10, 20]
        last_month = month_list.last()
        summary_list = []

        for year in years:
            # first month
            first_month_date = last_month.date - relativedelta(years=year-1, months=11)
            first_month = month_list.get(date=first_month_date)
            # months
            months = month_list.filter(date__gte=first_month_date)
            # summary
            summary = {}
            summary['year'] = year
            summary['base_date'] = first_month.date
            summary['base'] = first_month.base
            summary['high'] = months.order_by('-high').first().high
            summary['high_change'] = round((summary['high'] - summary['base']) / summary['base'] * 100, 2)
            summary['low'] = months.order_by('-low').last().low
            summary['low_change'] = round((summary['low'] - summary['base']) / summary['base'] * 100, 2)
            summary['close'] = last_month.close
            summary['close_change'] = round((summary['close'] - summary['base']) / summary['base'] * 100, 2)
            # summary list
            summary_list.append(summary)
        return summary_list


class IndexCycle(generic.DetailView):
    model = Index
    context_object_name = 'index'
    template_name = 'index/cycle.html'

    def get_context_data(self, **kwargs):
        # base 
        context = super(IndexCycle, self).get_context_data(**kwargs)
        # index object
        context_index = kwargs['object']
        # cycle list
        context['cycle_list'] = self.get_cycle_list(context_index)
        if context['cycle_list']:
            context['summary_list'] = self.get_summary_list(context['cycle_list'])
        return context

    def get_cycle_list(self, context_index):
        cycle_list = list(Cycle.objects.filter(index=context_index))
        last = cycle_list[-1]
        today = Day.objects.filter(index=context_index).last()

        # append today
        if today.date > last.date:
            if today.close != last.close:
                diff = today.close - last.close
                change = round(diff / last.close * 100, 2)
            else:
                diff = Decimal('0.00')
                change = Decimal('0.00')
            # cycle
            cycle = Cycle(date=today.date, base=last.close, close=today.close, \
                diff=diff, change=change, fix=False, index=context_index)
            # cycle list
            cycle_list.append(cycle)
        return cycle_list

    def get_summary_list(self, cycle_list):
        base_date = cycle_list[0].date
        close_date = base_date
        summary_list = []

        for cycle in cycle_list[1:]:
            # range
            base_date = close_date
            close_date = cycle.date
            period = relativedelta(close_date, base_date)
            # summary
            summary = {}
            summary['base_date'] = base_date
            summary['base'] = cycle.base
            summary['close_date'] = close_date
            summary['close'] = cycle.close
            summary['period'] = "{0}년 {1}개월 {2}일".format(period.years, period.months, period.days)
            summary['change'] = cycle.change 
            summary['fix'] = cycle.fix 
            # summary list
            summary_list.append(summary)
        return summary_list


class IndexExpiration(generic.DetailView):
    model = Index
    context_object_name = 'index'
    template_name = 'index/expiration.html'

    def get_context_data(self, **kwargs):
        # base 
        context = super(IndexExpiration, self).get_context_data(**kwargs)
        # index object
        context_index = kwargs['object']
        # expiration list
        context['expiration_list'] = Month.objects.filter(index=context_index)
        if context['expiration_list']:
            context['summary_list'] = self.get_summary_list(context['expiration_list'])
        return context

    def get_summary_list(self, expiration_list):
        pass

