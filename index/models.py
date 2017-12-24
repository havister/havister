"""havister index models
"""
from django.db import models

class Item(models.Model):
    """지수 구분"""
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    country = models.CharField(max_length=50)
    market = models.BooleanField(default=False)
    future = models.BooleanField(default=False)
    option = models.BooleanField(default=False)
    fund = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'index_item'

class AbstractPrice(models.Model):
    """abstract class"""
    date = models.DateField()
    code = models.ForeignKey('Item', on_delete=models.CASCADE)
    base = models.DecimalField(max_digits=7, decimal_places=2)
    open = models.DecimalField(max_digits=7, decimal_places=2)
    high = models.DecimalField(max_digits=7, decimal_places=2)
    low = models.DecimalField(max_digits=7, decimal_places=2)
    close = models.DecimalField(max_digits=7, decimal_places=2)
    difference = models.DecimalField(max_digits=6, decimal_places=2)
    change = models.DecimalField(verbose_name='change (%)', max_digits=5, decimal_places=2)

    def __str__(self):
        return self.code

    class Meta:
        abstract = True

class CalendarMonth(AbstractPrice):
    """달력월"""
    class Meta:
        db_table = 'index_calendar_month'

class SettlementMonth(AbstractPrice):
    """결제월"""
    class Meta:
        db_table = 'index_settlement_month'

