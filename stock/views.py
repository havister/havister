"""havister stock views
"""
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views import generic

from .models import Stock, Day, Month, Cycle, Expiration

class ListView(generic.ListView):
    context_object_name = 'stock_list'
    template_name = 'stock/list.html'

    def get_queryset(self):
        return Stock.objects.filter(option=True)


class MonthView(generic.DetailView):
    pass


class CycleView(generic.DetailView):
    pass


class ExpirationView(generic.DetailView):
    pass

