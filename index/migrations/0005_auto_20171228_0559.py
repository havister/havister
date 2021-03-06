# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-27 20:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_auto_20171226_0351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('close', models.DecimalField(decimal_places=2, max_digits=7)),
                ('index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Index')),
            ],
            options={
                'db_table': 'index_daily',
            },
        ),
        migrations.RenameModel(
            old_name='CalendarMonth',
            new_name='CalendarMonthly',
        ),
        migrations.RenameModel(
            old_name='SettlementMonth',
            new_name='SettlementMonthly',
        ),
        migrations.AlterModelTable(
            name='calendarmonthly',
            table='index_calendar_monthly',
        ),
        migrations.AlterModelTable(
            name='settlementmonthly',
            table='index_settlement_monthly',
        ),
    ]
