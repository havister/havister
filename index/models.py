"""havister index models
"""
from django.db import models

class Index(models.Model):
    """지수"""
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
        db_table = 'index'
        verbose_name = 'index'
        verbose_name_plural = 'indices'

class AbstractBC(models.Model):
    """abstract base-close"""
    date = models.DateField()
    index = models.ForeignKey('Index', on_delete=models.CASCADE)
    base = models.DecimalField(max_digits=7, decimal_places=2)
    close = models.DecimalField(max_digits=7, decimal_places=2)
    difference = models.DecimalField(max_digits=7, decimal_places=2)
    change = models.DecimalField('change (%)', max_digits=5, decimal_places=2)

    def __str__(self):
        return self.index

    class Meta:
        abstract = True

class AbstractBOHLC(models.Model):
    """abstract base-open-high-low-close"""
    date = models.DateField()
    index = models.ForeignKey('Index', on_delete=models.CASCADE)
    base = models.DecimalField(max_digits=7, decimal_places=2)
    open = models.DecimalField(max_digits=7, decimal_places=2)
    high = models.DecimalField(max_digits=7, decimal_places=2)
    low = models.DecimalField(max_digits=7, decimal_places=2)
    close = models.DecimalField(max_digits=7, decimal_places=2)
    difference = models.DecimalField(max_digits=7, decimal_places=2)
    change = models.DecimalField('change (%)', max_digits=5, decimal_places=2)

    def __str__(self):
        return self.index

    class Meta:
        abstract = True

class Day(AbstractBOHLC):
    """일간"""
    class Meta:
        db_table = 'index_day'
        verbose_name = 'day'
        verbose_name_plural = 'days'

class TwelveReversal(AbstractBC):
    """12(%) 전환"""
    class Meta:
        db_table = 'index_twelve_reversal'
        verbose_name = 'twelve reversal'
        verbose_name_plural = 'twelve reversals'

class CalendarMonth(AbstractBOHLC):
    """달력 월간"""
    class Meta:
        db_table = 'index_calendar_month'
        verbose_name = 'calendar month'
        verbose_name_plural = 'calendar months'

class SettlementMonth(AbstractBOHLC):
    """결제 월간"""
    class Meta:
        db_table = 'index_settlement_month'
        verbose_name = 'settlement month'
        verbose_name_plural = 'settlement months'

