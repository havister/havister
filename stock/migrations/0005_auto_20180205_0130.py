# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-04 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_auto_20180131_0325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cycle',
            old_name='fix',
            new_name='certainty',
        ),
        migrations.RemoveField(
            model_name='day',
            name='change',
        ),
        migrations.AlterField(
            model_name='day',
            name='diff',
            field=models.IntegerField(null=True),
        ),
    ]