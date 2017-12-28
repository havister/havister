"""havister index admin
"""
from django.contrib import admin

from . import models

admin.site.register(models.Index)
admin.site.register(models.Day)
admin.site.register(models.TwelveReversal)
admin.site.register(models.CalendarMonth)
admin.site.register(models.SettlementMonth)

