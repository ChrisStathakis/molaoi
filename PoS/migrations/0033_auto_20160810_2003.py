# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-10 17:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PoS', '0032_auto_20160810_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lianiki_order',
            name='day_added',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 10, 20, 3, 40, 338237)),
        ),
        migrations.AlterField(
            model_name='lianiki_order',
            name='title',
            field=models.CharField(default=datetime.datetime(2016, 8, 10, 20, 3, 40, 338237), max_length=50),
        ),
    ]
