"""havister index urls
"""
from django.conf.urls import url

from .views import IndexList, IndexDetail

app_name = 'index'

urlpatterns = [
    url(r'^$', IndexList.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', IndexDetail.as_view(), name='detail'),
]

