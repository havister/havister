"""havister stock models
"""
from django.db import models

class AbstractOHLC(models.Model):
    """abstract"""
    date = models.DateField()
    open = models.PositiveIntegerField()
    high = models.PositiveIntegerField()
    low = models.PositiveIntegerField()
    close = models.PositiveIntegerField()
    change = models.DecimalField('change(%)', max_digits=7, decimal_places=2)
    stock = models.ForeignKey('Stock', db_column='stock_code', on_delete=models.CASCADE, unique_for_date='date')

    def __str__(self):
        return "{0} ({1})".format(self.date, self.index)

    class Meta:
        abstract = True


class Stock(models.Model):
    """주식"""
    # country choice
    KOREA = '한국'
    AMERICA = '미국'
    CHINA = '중국'
    JAPAN = '일본'
    COUNTRY_CHOICES = (
        (KOREA, '한국'),
        (AMERICA, '미국'),
        (CHINA, '중국'),
        (JAPAN, '일본'),
    )
    # market choice
    KOSPI = 'KOSPI'
    KOSDAQ = 'KOSDAQ'
    MARKET_CHOICES = (
        (KOSPI, 'KOSPI'),
        (KOSDAQ, 'KOSDAQ'),
    )
    # filed
    code = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default=KOREA)
    market = models.CharField(max_length=6, choices=MARKET_CHOICES, default=KOSPI)
    future = models.BooleanField(default=False)
    option = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'stock'
        ordering = ['name']
        verbose_name = 'stock'
        verbose_name_plural = 'stocks'


class Day(models.Model):
    """일간"""
    date = models.DateField()
    open = models.PositiveIntegerField()
    high = models.PositiveIntegerField()
    low = models.PositiveIntegerField()
    close = models.PositiveIntegerField()
    diff = models.IntegerField()
    change = models.DecimalField('change(%)', max_digits=7, decimal_places=2)
    stock = models.ForeignKey('Stock', db_column='stock_code', on_delete=models.CASCADE, unique_for_date='date')

    def __str__(self):
        return "{0} ({1})".format(self.date, self.stock)

    class Meta:
        db_table = 'stock_day'
        ordering = ['date']
        verbose_name = 'day'
        verbose_name_plural = 'days'


class Month(AbstractOHLC):
    """월간"""
    class Meta:
        db_table = 'stock_month'
        ordering = ['date']
        verbose_name = 'month'
        verbose_name_plural = 'months'


class Cycle(models.Model):
    """순환(-30%:하락전환)"""
    date = models.DateField()
    close = models.PositiveIntegerField()
    change = models.DecimalField('change(%)', max_digits=7, decimal_places=2)
    fix = models.BooleanField(default=False)
    stock = models.ForeignKey('Stock', db_column='stock_code', on_delete=models.CASCADE, unique_for_date='date')

    def __str__(self):
        return "{0} ({1})".format(self.date, self.index)

    class Meta:
        db_table = 'stock_cycle'
        ordering = ['date']
        verbose_name = 'cycle'
        verbose_name_plural = 'cycles'


class Expiration(AbstractOHLC):
    """만기(월간)"""
    class Meta:
        db_table = 'stock_expiration'
        ordering = ['date']
        verbose_name = 'expiration'
        verbose_name_plural = 'expirations'

