"""havister index models
"""
from django.db import models

class Item(models.Model):
    """index item
    """
<<<<<<< HEAD
    code = models.CharField(max_length=10, unique=True)
=======
    code = models.CharField(max_length=6, unique=True)
>>>>>>> 925ff23e104f0b9d3681fd2edcbdffb211034959
    name = models.SlugField(max_length=50)
    market = models.BooleanField(default=False)
    future = models.BooleanField(default=False)
    option = models.BooleanField(default=False)
    fund = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'index_item'
