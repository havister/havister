# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-15 20:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0021_auto_20180116_0402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='diff',
        ),
    ]
