"""havister index views
"""
from dateutil.relativedelta import relativedelta
from django.views import generic

from .models import Index, Day, Month, Reversal, Settlement

class IndexList(generic.ListView):
    context_object_name = 'index_list'
    template_name = 'index/list.html'

    def get_queryset(self):
        return Index.objects.order_by('-market', '-future', '-option', '-fund')

class IndexDetail(generic.DetailView):
    context_object_name = 'index'
    model = Index
    template_name = 'index/detail.html'

    def get_context_data(self, **kwargs):
        # base 
        context = super(IndexDetail, self).get_context_data(**kwargs)
        # extra
        context_index = kwargs['object']
        context['month_list'] = Month.objects.filter(index=context_index)
        context['month_summary_list'] = self.get_month_summary_list()
        context['reversal_list'] = Reversal.objects.filter(index=context_index)
        return context

    def get_month_summary_list(self):
        years = [1, 3, 5, 10]
        last_month = Month.objects.order_by('date').last()
        summary_list = []

        for year in years:
            # first month
            first_month_date = last_month.date - relativedelta(years=year-1, months=11)
            first_month = Month.objects.get(date=first_month_date)
            # months
            months = Month.objects.filter(date__gte=first_month_date)
            # summary
            summary = {}
            summary['year'] = year
            summary['base'] = first_month.base
            summary['high'] = months.order_by('-high').first().high
            summary['high_diff'] = summary['high'] - summary['base']
            summary['high_change'] = round(summary['high_diff'] / summary['base'] * 100, 2)
            summary['low'] = months.order_by('-low').last().low
            summary['low_diff'] = summary['low'] - summary['base']
            summary['low_change'] = round(summary['low_diff'] / summary['base'] * 100, 2)
            summary['close'] = last_month.close
            summary['close_diff'] = summary['close'] - summary['base']
            summary['close_change'] = round(summary['close_diff'] / summary['base'] * 100, 2)
            # summary_list
            summary_list.append(summary)
        return summary_list

