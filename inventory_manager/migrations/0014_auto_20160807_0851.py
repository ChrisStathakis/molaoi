# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-07 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_manager', '0013_auto_20160807_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendordepositorderpay',
            name='day_added',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='vendordepositorderpay',
            name='title_de',
            field=models.CharField(blank=True, max_length=64, verbose_name='Σχόλια'),
        ),
    ]
