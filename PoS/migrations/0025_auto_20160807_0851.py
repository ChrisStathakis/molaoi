# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-07 05:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PoS', '0024_auto_20160807_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lianiki_order',
            name='day_added',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 7, 8, 51, 45, 411709)),
        ),
        migrations.AlterField(
            model_name='lianiki_order',
            name='title',
            field=models.CharField(default=datetime.datetime(2016, 8, 7, 8, 51, 45, 411709), max_length=50),
        ),
    ]
