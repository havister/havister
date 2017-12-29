"""havister index views
"""
from django.shortcuts import get_object_or_404
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
        context['reversal_list'] = Reversal.objects.filter(index=context_index)
        context['settlement_list'] = Settlement.objects.filter(index=context_index)
        return context

