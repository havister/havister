# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-10 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expiration',
            fields=[
                ('month', models.DateField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'expirations',
                'ordering': ['month'],
                'db_table': 'expiration',
                'verbose_name': 'expiration',
            },
        ),
    ]
