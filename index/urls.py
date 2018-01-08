"""havister index urls
"""
from django.conf.urls import url

from .views import IndexList, IndexBasic, IndexCycle, IndexExpiration 

app_name = 'index'

urlpatterns = [
    url(r'^$', IndexList.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', IndexBasic.as_view(), name='basic'),
    url(r'^(?P<slug>[\w-]+)/cycle/$', IndexCycle.as_view(), name='cycle'),
    url(r'^(?P<slug>[\w-]+)/expiration/$', IndexExpiration.as_view(), name='expiration'),
]

