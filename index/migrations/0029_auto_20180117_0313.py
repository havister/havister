# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-16 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0028_auto_20180117_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='index',
            name='type',
            field=models.CharField(choices=[('종합', '종합'), ('대표', '대표'), ('업종', '업종'), ('테마', '테마'), ('미정', '미정')], default='미정', max_length=2),
        ),
    ]
