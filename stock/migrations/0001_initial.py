# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-21 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('country', models.CharField(choices=[('한국', '한국'), ('미국', '미국'), ('중국', '중국'), ('일본', '일본')], default='한국', max_length=2)),
                ('market', models.CharField(choices=[('KOSPI', 'KOSPI'), ('KOSDAQ', 'KOSDAQ')], default='KOSPI', max_length=6)),
                ('future', models.BooleanField(default=False)),
                ('option', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'stock',
                'verbose_name_plural': 'stocks',
                'verbose_name': 'stock',
                'ordering': ['name'],
            },
        ),
    ]
