# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-01 19:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PoS', '0018_auto_20160731_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyincomegreg',
            name='title',
            field=models.CharField(default='2016-08-01', max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='lianiki_order',
            name='day_added',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 1, 22, 17, 50, 818462)),
        ),
        migrations.AlterField(
            model_name='lianiki_order',
            name='title',
            field=models.CharField(default=datetime.datetime(2016, 8, 1, 22, 17, 50, 818462), max_length=50),
        ),
        migrations.AlterField(
            model_name='monthlyincomegreg',
            name='title',
            field=models.CharField(default='August', max_length=64),
        ),
    ]
