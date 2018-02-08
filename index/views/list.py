"""havister index views
"""
from django.views import generic

from index.models import Index

class ListView(generic.ListView):
    context_object_name = 'index_list'
    template_name = 'index/list.html'

    def get_queryset(self):
        return Index.objects.all()

