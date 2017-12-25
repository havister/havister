"""havister index admin
"""
from django.contrib import admin

from .models import Index, CalendarMonth, SettlementMonth

admin.site.register(Index)
admin.site.register(CalendarMonth)
admin.site.register(SettlementMonth)

