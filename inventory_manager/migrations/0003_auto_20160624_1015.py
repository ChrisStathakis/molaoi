# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-24 07:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_manager', '0002_auto_20160607_0844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Τιμολόγια   '},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['product'], 'verbose_name': 'Συστατικά Τιμολογίου   '},
        ),
        migrations.AlterModelOptions(
            name='payorders',
            options={'verbose_name': 'Εντολές Πληρωμής    '},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'ordering': ['name'], 'verbose_name': 'Μονάδα Μέτρησης  '},
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='taxes',
            field=models.CharField(choices=[('a', '13'), ('b', '23'), ('c', '24'), ('d', '0')], default='b', max_length=1, verbose_name='ΦΠΑ'),
        ),
    ]
