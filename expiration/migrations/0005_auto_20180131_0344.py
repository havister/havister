# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-30 18:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expiration', '0004_auto_20180127_0452'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Expiration',
            new_name='Period',
        ),
        migrations.AlterModelOptions(
            name='period',
            options={'ordering': ['month'], 'verbose_name': 'period', 'verbose_name_plural': 'periods'},
        ),
        migrations.AlterModelTable(
            name='period',
            table='expiration_period',
        ),
    ]
