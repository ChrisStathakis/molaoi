# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-29 09:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PoS', '0066_auto_20170701_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyincomegreg',
            name='title',
            field=models.CharField(default='2017-09-29', max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='lianiki_order',
            name='day_added',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 29, 12, 49, 7, 966911)),
        ),
        migrations.AlterField(
            model_name='lianiki_order',
            name='title',
            field=models.CharField(default=datetime.datetime(2017, 9, 29, 12, 49, 7, 966911), max_length=50),
        ),
        migrations.AlterField(
            model_name='monthlyincomegreg',
            name='title',
            field=models.CharField(default='September', max_length=64),
        ),
    ]
