"""havister stock models
"""
from django.db import models

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

