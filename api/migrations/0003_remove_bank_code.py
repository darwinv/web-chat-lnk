# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-05 19:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180905_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='code',
        ),
    ]
