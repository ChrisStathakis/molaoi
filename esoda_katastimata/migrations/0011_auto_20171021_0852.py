# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-21 05:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esoda_katastimata', '0010_auto_20170929_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthesoda',
            name='title',
            field=models.CharField(default='October', max_length=64),
        ),
    ]