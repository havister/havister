"""havister index urls
"""
from django.conf.urls import url

from .views import ListView, BasicView, CycleView, ExpirationView 

app_name = 'index'

urlpatterns = [
    url(r'^$', ListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', BasicView.as_view(), name='basic'),
    url(r'^(?P<slug>[\w-]+)/cycle/$', CycleView.as_view(), name='cycle'),
    url(r'^(?P<slug>[\w-]+)/expiration/$', ExpirationView.as_view(), name='expiration'),
]

