# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-07 05:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transcations', '0008_auto_20160531_2348'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagia_Exoda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True, verbose_name='')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Σημειώσεις')),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Συνολικά Έξοδα')),
                ('remaining_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Υπόλοιπο')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transcations.Fixed_costs')),
            ],
        ),
    ]
