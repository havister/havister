# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-23 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0030_auto_20180117_0315'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='diff',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
