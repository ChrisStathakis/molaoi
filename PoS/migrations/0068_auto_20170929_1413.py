# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-29 11:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PoS', '0067_auto_20170929_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lianiki_order',
            name='day_added',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 29, 14, 13, 46, 450183)),
        ),
        migrations.AlterField(
            model_name='lianiki_order',
            name='title',
            field=models.CharField(default=datetime.datetime(2017, 9, 29, 14, 13, 46, 450183), max_length=50),
        ),
    ]