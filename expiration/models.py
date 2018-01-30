"""havister expiration models
"""
from django.db import models

class Period(models.Model):
    """만기기간"""
    month = models.DateField(primary_key=True)
    open_date = models.DateField()
    close_date = models.DateField()

    def __str__(self):
        return "{0}년 {1}월".format(self.month.year, self.month.month)

    class Meta:
        db_table = 'expiration_period'
        ordering = ['month']
        verbose_name = 'period'
        verbose_name_plural = 'periods'

