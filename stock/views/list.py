"""havister stock views
"""
from django.views import generic

from stock.models import Stock

class ListView(generic.ListView):
    context_object_name = 'stock_list'
    template_name = 'stock/list.html'

    def get_queryset(self):
        return Stock.objects.filter(option=True)

