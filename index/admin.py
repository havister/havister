"""havister index admin
"""
from django.contrib import admin

from . import models

admin.site.register(models.Index)
admin.site.register(models.Day)
admin.site.register(models.Month)
admin.site.register(models.Cycle)
admin.site.register(models.Expiration)

