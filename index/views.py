"""havister index views
"""
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views import generic

from .models import Index, Day, Month, Cycle, Expiration

class ListView(generic.ListView):
    context_object_name = 'index_list'
    template_name = 'index/list.html'

    def get_queryset(self):
        return Index.objects.all()


class MonthView(generic.DetailView):
    model = Index
    context_object_name = 'index'
    template_name = 'index/month.html'

    def get_context_data(self, **kwargs):
        # base 
        context = super(MonthView, self).get_context_data(**kwargs)
        # index object
        index = kwargs['object']
        # month list
        context['detail_list'] = Month.objects.filter(index=index)
        # alpha list 
        if context['detail_list']:
            context['alpha_list'] = self.get_alpha_list(context['detail_list'])
        return context

    def get_alpha_list(self, month_list):
        years = [1, 3, 5, 10, 20]
        last_month = month_list.last()
        alpha_list = []

        for year in years:
            # base month
            base_month_date = last_month.date - relativedelta(years=year-1, months=12)
            try:
                base_month = month_list.get(date=base_month_date)
            except ObjectDoesNotExist:
                continue
            base = base_month.close
            # subset month list
            months = month_list.filter(date__gt=base_month_date)
            # alpha
            alpha = {}
            alpha['year'] = year
            alpha['first_date'] = months.first().date
            alpha['high'] = months.order_by('-high').first().high
            alpha['high_change'] = round((alpha['high'] - base) / base * 100, 2)
            alpha['low'] = months.order_by('-low').last().low
            alpha['low_change'] = round((alpha['low'] - base) / base * 100, 2)
            alpha['close'] = last_month.close
            alpha['close_change'] = round((alpha['close'] - base) / base * 100, 2)
            # alpha list
            alpha_list.append(alpha)
        return alpha_list


class CycleView(generic.DetailView):
    model = Index
    context_object_name = 'index'
    template_name = 'index/cycle.html'

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
                diff = today.close - last.close
                change = round(diff / last.close * 100, 2)
            else:
                diff = Decimal('0.00')
                change = Decimal('0.00')
            # cycle
            cycle = Cycle(date=today.date, close=today.close, change=change, fix=False, index=index)
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
            # alpha
            alpha = {}
            alpha['base_date'] = base_date
            alpha['close_date'] = close_date
            alpha['period'] = "{0}년 {1}개월 {2}일".format(period.years, period.months, period.days)
            alpha['close'] = cycle.close
            alpha['change'] = cycle.change 
            alpha['fix'] = cycle.fix 
            # alpha list
            alpha_list.append(alpha)
        return alpha_list


class ExpirationView(generic.DetailView):
    model = Index
    context_object_name = 'index'
    template_name = 'index/expiration.html'

    def get_context_data(self, **kwargs):
        # base 
        context = super(ExpirationView, self).get_context_data(**kwargs)
        # index object
        index = kwargs['object']
        if not index.future:
            raise Http404
        # expiration list
        context['detail_list'] = Expiration.objects.filter(index=index).reverse()[:12]
        # max period: 120 months
        period = Expiration.objects.filter(index=index).count()
        if period > 120:
            period = 120
        context['period'] = period
        # alpha, beta list
        if context['detail_list']:
            context['alpha_list'] = self.get_alpha_list(index, period)
            context['beta_list'] = self.get_beta_list(index, period)
        return context

    def get_alpha_list(self, index, period):
        # 변화율 분포
        start_at = Expiration.objects.filter(index=index).reverse()[period-1].date
        levels = [[100, 20], [20, 10], [10, 5], [5, 0], [0, 0], [0, -5], [-5, -10], [-10, -20], [-20, -100]]
        alpha_list = []

        for level in levels:
            # level
            high = level[0]
            low = level[1]
            # alpha
            alpha = {}
            if high > 0:
                if high < 100:
                    alpha['level'] = "상승 {0}% 미만".format(high)
                else:
                    alpha['level'] = "상승 {0}% 이상".format(low)
                alpha['count'] = Expiration.objects.filter(index=index, date__gte=start_at, change__lt=high, change__gte=low).count()
            elif high == 0 and low == 0:
                alpha['level'] = "보합 0%"
                alpha['count'] = Expiration.objects.filter(index=index, date__gte=start_at, change=0).count()
            elif low < 0:
                if low > -100:
                    alpha['level'] = "하락 {0}% 미만".format(abs(low))
                else:
                    alpha['level'] = "하락 {0}% 이상".format(abs(high))
                alpha['count'] = Expiration.objects.filter(index=index, date__gte=start_at, change__lte=high, change__gt=low).count()
            # alpha list
            alpha_list.append(alpha)
        return alpha_list

    def get_beta_list(self, index, period):
        # 변화율 리스트
        beta_list = Expiration.objects.filter(index=index).values('change').reverse()[:period]
        return beta_list

