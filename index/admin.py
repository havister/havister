"""havister index admin
"""
from django.contrib import admin

from .models import Item, CalendarMonth, SettlementMonth

admin.site.register(Item)
admin.site.register(CalendarMonth)
admin.site.register(SettlementMonth)

