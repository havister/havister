"""havister index urls
"""
from django.conf.urls import url

from .views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
]

