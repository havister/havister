# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-11 18:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0017_auto_20180110_0059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day',
            options={'ordering': ['date'], 'verbose_name': 'day', 'verbose_name_plural': 'days'},
        ),
        migrations.AlterModelOptions(
            name='expiration',
            options={'ordering': ['date'], 'verbose_name': 'expiration', 'verbose_name_plural': 'expirations'},
        ),
        migrations.AlterModelOptions(
            name='month',
            options={'ordering': ['date'], 'verbose_name': 'month', 'verbose_name_plural': 'months'},
        ),
    ]
