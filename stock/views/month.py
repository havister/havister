"""havister stock views
"""
import decimal
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ObjectDoesNotExist
from django.views import generic

from stock.models import Stock, Day, Month

class MonthView(generic.DetailView):
    model = Stock
    context_object_name = 'stock'
    template_name = 'stock/month.html'

    def __init__(self):
        dc = decimal.getcontext()
        dc.prec = 9
        dc.rounding = decimal.ROUND_HALF_UP

    def get_context_data(self, **kwargs):
        # base
        context = super(MonthView, self).get_context_data(**kwargs)
        # stock object
        stock = kwargs['object']
        # month list
        context['detail_list'] = Month.objects.filter(stock=stock)
        # extra
        if context['detail_list']:
            context['max_date'] = context['detail_list'].last().date + relativedelta(years=1)
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
            alpha['high_change'] = round(Decimal(str((alpha['high'] - base) / base)) * 100, 2)
            alpha['low'] = months.order_by('-low').last().low
            alpha['low_change'] = round(Decimal(str((alpha['low'] - base) / base)) * 100, 2)
            alpha['close'] = last_month.close
            alpha['close_change'] = round(Decimal(str((alpha['close'] - base) / base)) * 100, 2)
            # alpha list
            alpha_list.append(alpha)
        return alpha_list

