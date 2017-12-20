"""havister index urls
"""
from django.conf.urls import url

from .views import HomeView

app_name = 'index'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
]

