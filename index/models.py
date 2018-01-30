"""havister index models
"""
from django.db import models

class AbstractOHLC(models.Model):
    """abstract"""
    date = models.DateField()
    open = models.DecimalField(max_digits=7, decimal_places=2)
    high = models.DecimalField(max_digits=7, decimal_places=2)
    low = models.DecimalField(max_digits=7, decimal_places=2)
    close = models.DecimalField(max_digits=7, decimal_places=2)
    change = models.DecimalField('change(%)', max_digits=7, decimal_places=2)
    index = models.ForeignKey('Index', db_column='index_code', on_delete=models.CASCADE, unique_for_date='date')

    def __str__(self):
        return "{0} ({1})".format(self.date, self.index)

    class Meta:
        abstract = True


class Index(models.Model):
    """지수"""
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
    # type choice
    COMPOSITE = '종합'
    BLUECHIP = '대표'
    SECTOR = '업종'
    THEMATICS = '테마'
    UNKNOWN = '미정'
    TYPE_CHOICES = (
        (COMPOSITE, '종합'),
        (BLUECHIP, '대표'),
        (SECTOR, '업종'),
        (THEMATICS, '테마'),
        (UNKNOWN, '미정'),
    )
    # filed
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default=KOREA)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=UNKNOWN)
    future = models.BooleanField(default=False)
    option = models.BooleanField(default=False)
    etf = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'index'
        ordering = ['code']
        verbose_name = 'index'
        verbose_name_plural = 'indices'


class Day(models.Model):
    """일간"""
    date = models.DateField()
    open = models.DecimalField(max_digits=7, decimal_places=2)
    high = models.DecimalField(max_digits=7, decimal_places=2)
    low = models.DecimalField(max_digits=7, decimal_places=2)
    close = models.DecimalField(max_digits=7, decimal_places=2)
    diff = models.DecimalField(max_digits=7, decimal_places=2)
    change = models.DecimalField('change(%)', max_digits=7, decimal_places=2)
    index = models.ForeignKey('Index', db_column='index_code', on_delete=models.CASCADE, unique_for_date='date')

    def __str__(self):
        return "{0} ({1})".format(self.date, self.index)

    class Meta:
        db_table = 'index_day'
        ordering = ['date']
        verbose_name = 'day'
        verbose_name_plural = 'days'


class Month(AbstractOHLC):
    """월간"""
    class Meta:
        db_table = 'index_month'
        ordering = ['date']
        verbose_name = 'month'
        verbose_name_plural = 'months'


class Cycle(models.Model):
    """순환(-30%:하락전환)"""
    date = models.DateField()
    close = models.DecimalField(max_digits=7, decimal_places=2)
    change = models.DecimalField('change(%)', max_digits=7, decimal_places=2)
    fix = models.BooleanField(default=False)
    index = models.ForeignKey('Index', db_column='index_code', on_delete=models.CASCADE, unique_for_date='date')

    def __str__(self):
        return "{0} ({1})".format(self.date, self.index)

    class Meta:
        db_table = 'index_cycle'
        ordering = ['date']
        verbose_name = 'cycle'
        verbose_name_plural = 'cycles'


class Expiration(AbstractOHLC):
    """만기(월간)"""
    class Meta:
        db_table = 'index_expiration'
        ordering = ['date']
        verbose_name = 'expiration'
        verbose_name_plural = 'expirations'

