# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-06 08:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20160904_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeQtyOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True)),
                ('day_added', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChangeQtyOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ChangeQtyOrder')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
    ]
