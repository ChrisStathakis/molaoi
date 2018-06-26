# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-31 10:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_manager', '0006_auto_20160731_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethodGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='payment_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory_manager.PaymentMethodGroup'),
        ),
    ]
