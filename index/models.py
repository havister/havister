"""havister index models
"""
from django.db import models

class Item(models.Model):
    """index item
    """
    code = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=50)
    future = models.BooleanField(default=False)
    option = models.BooleanField(default=False)
    fund = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'index_item'

