# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-30 01:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0009_auto_20171230_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='change',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='change(%)'),
        ),
        migrations.AlterField(
            model_name='month',
            name='change',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='change(%)'),
        ),
        migrations.AlterField(
            model_name='reversal',
            name='change',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='change(%)'),
        ),
        migrations.AlterField(
            model_name='settlement',
            name='change',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='change(%)'),
        ),
    ]