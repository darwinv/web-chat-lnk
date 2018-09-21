# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-21 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20180921_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.FloatField(verbose_name='amount'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='observations',
            field=models.CharField(max_length=255, null=True, verbose_name='observations'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='operation_number',
            field=models.CharField(max_length=12, verbose_name='operation number'),
        ),
    ]
