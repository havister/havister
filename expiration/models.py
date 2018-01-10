"""havister expiration models
"""
from django.db import models

class Expiration(models.Model):
    """만기"""
    month = models.DateField(primary_key=True)
    open_date = models.DateField()
    close_date = models.DateField()

    def __str__(self):
        return "{0}년 {1}월".format(self.month.year, self.month.month)

    class Meta:
        db_table = 'expiration'
        verbose_name = 'expiration'
        verbose_name_plural = 'expirations'
        ordering = ['month']

