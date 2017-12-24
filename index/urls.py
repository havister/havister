"""havister index urls
"""
from django.conf.urls import url

from .views import HomeView, DetailView

app_name = 'index'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^(?P<slug>[\w-]+)/$', DetailView.as_view(), name='detail'),
]

