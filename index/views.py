"""havister index views
"""
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Index, CalendarMonth, SettlementMonth

class ListView(generic.ListView):
    template_name = 'index/list.html'
    context_object_name = 'index_list'

    def get_queryset(self):
        return Index.objects.order_by('-market', '-future', '-option', '-fund')

class DetailView(generic.ListView):
    template_name = 'index/detail.html'
    context_object_name = 'index_detail'

    def get_queryset(self):
        self.index = get_object_or_404(Index, slug=self.kwargs['slug'])
        return CalendarMonth.objects.filter(index=self.index)

