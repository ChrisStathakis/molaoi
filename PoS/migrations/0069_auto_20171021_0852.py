# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-21 05:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PoS', '0068_auto_20170929_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyincomegreg',
            name='title',
            field=models.CharField(default='2017-10-21', max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='lianiki_order',
            name='day_added',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 21, 8, 52, 37, 861743)),
        ),
        migrations.AlterField(
            model_name='lianiki_order',
            name='title',
            field=models.CharField(default=datetime.datetime(2017, 10, 21, 8, 52, 37, 861743), max_length=50),
        ),
        migrations.AlterField(
            model_name='monthlyincomegreg',
            name='title',
            field=models.CharField(default='October', max_length=64),
        ),
    ]