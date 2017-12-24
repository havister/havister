"""havister index views
"""
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Item, CalendarMonth, SettlementMonth

class HomeView(generic.ListView):
    template_name = 'index/home.html'
    context_object_name = 'item_list'

    def get_queryset(self):
        return Item.objects.order_by('name')

class DetailView(generic.TemplateView):
    template_name = 'index/detail.html'

