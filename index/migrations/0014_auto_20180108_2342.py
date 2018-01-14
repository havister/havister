# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-08 14:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0013_auto_20180108_0238'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reversal',
            new_name='Cycle',
        ),
        migrations.RenameModel(
            old_name='Settlement',
            new_name='Expiration',
        ),
        migrations.AlterModelOptions(
            name='cycle',
            options={'verbose_name': 'cycle', 'verbose_name_plural': 'cycles'},
        ),
        migrations.AlterModelOptions(
            name='expiration',
            options={'verbose_name': 'expiration', 'verbose_name_plural': 'expirations'},
        ),
        migrations.AlterModelTable(
            name='cycle',
            table='index_cycle',
        ),
        migrations.AlterModelTable(
            name='expiration',
            table='index_expiration',
        ),
    ]