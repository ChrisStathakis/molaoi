# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-26 05:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PoS', '0007_lianiki_order_lianikiorderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='lianikiorderitem',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='lianikiorderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='dailyincomegreg',
            name='title',
            field=models.CharField(default='2016-06-26', max_length=64, unique=True),
        ),
    ]