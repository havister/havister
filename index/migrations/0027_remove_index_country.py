# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-16 18:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0026_remove_index_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='index',
            name='country',
        ),
    ]
