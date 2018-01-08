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
        # index
        context_index = kwargs['object']
        # month_list
        context['month_list'] = Month.objects.filter(index=context_index)
        if context['month_list']:
            context['month_summary_list'] = self.get_month_summary_list(context['month_list'])
        # reversal_list
        context['reversal_list'] = Reversal.objects.filter(index=context_index)
        if context['reversal_list']:
            context['reversal_summary_list'] = self.get_reversal_summary_list(context['reversal_list'])
        return context

    def get_month_summary_list(self, month_list):
        years = [1, 3, 5, 10]
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
            summary['base'] = first_month.base
            summary['high'] = months.order_by('-high').first().high
            summary['high_change'] = round((summary['high'] - summary['base']) / summary['base'] * 100, 2)
            summary['low'] = months.order_by('-low').last().low
            summary['low_change'] = round((summary['low'] - summary['base']) / summary['base'] * 100, 2)
            summary['close'] = last_month.close
            summary['close_change'] = round((summary['close'] - summary['base']) / summary['base'] * 100, 2)
            # summary_list
            summary_list.append(summary)
        return summary_list

    def get_reversal_summary_list(self, reversal_list):
        start_date = reversal_list.first().date
        end_date = start_date
        summary_list = []

        for no, reversal in enumerate(reversal_list[1:]):
            # range
            start_date = end_date
            end_date = reversal.date
            period = relativedelta(end_date, start_date)
            # summary
            summary = {}
            summary['no'] = no + 1
            summary['start_date'] = start_date
            summary['end_date'] = end_date
            summary['period'] = "{0}년 {1}개월 {2}일".format(period.years, period.months, period.days)
            summary['change'] = reversal.change 
            # summary_list
            summary_list.append(summary)
        return summary_list

