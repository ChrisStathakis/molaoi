# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-06 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esoda_katastimata', '0012_auto_20180406_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='addesoda',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='Σχόλια'),
        ),
        migrations.AlterField(
            model_name='yearesoda',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='Σχόλια'),
        ),
    ]
