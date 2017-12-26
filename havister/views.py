"""havister root views
"""
from django.shortcuts import render
from django.views import generic

class HomeView(generic.TemplateView):
    template_name = 'home.html'

def bad_request_view(request):
    return render(request, '400.html')

def permission_denied_view(request):
    return render(request, '403.html')

def page_not_found_view(request):
    return render(request, '404.html')

def server_error_view(request):
    return render(request, '500.html')

