# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-07 05:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(max_length=40, unique=True, verbose_name='Αριθμός Παραστατικού'),
        ),
    ]
