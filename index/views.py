"""havister index views
"""
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Item

class HomeView(generic.TemplateView):
    template_name = 'index/home.html'

