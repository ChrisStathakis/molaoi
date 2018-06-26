# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-07 08:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_manager', '0016_auto_20160807_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='payorders',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory_manager.PaymentMethod'),
        ),
    ]