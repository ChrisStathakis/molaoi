# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-10 15:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PoS', '0030_auto_20160810_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lianiki_order',
            name='day_added',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 10, 18, 48, 19, 412464)),
        ),
        migrations.AlterField(
            model_name='lianiki_order',
            name='title',
            field=models.CharField(default=datetime.datetime(2016, 8, 10, 18, 48, 19, 412464), max_length=50),
        ),
    ]