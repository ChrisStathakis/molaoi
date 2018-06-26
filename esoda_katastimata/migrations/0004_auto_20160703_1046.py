# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-03 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esoda_katastimata', '0003_auto_20160703_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addesoda',
            name='title',
            field=models.DateField(verbose_name='Ημερομηνία'),
        ),
        migrations.AlterField(
            model_name='yearesoda',
            name='title',
            field=models.CharField(default='2016', max_length=64, unique=True),
        ),
    ]
