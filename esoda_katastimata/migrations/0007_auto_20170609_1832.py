# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-09 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esoda_katastimata', '0006_auto_20161207_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='yearesoda',
            name='boom_income',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='monthesoda',
            name='title',
            field=models.CharField(default='June', max_length=64),
        ),
        migrations.AlterField(
            model_name='yearesoda',
            name='title',
            field=models.CharField(default='2017', max_length=64, unique=True),
        ),
    ]
