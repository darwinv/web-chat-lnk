# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-06 21:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20171201_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='commercial_reason',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='img_document_number',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='key',
            field=models.CharField(blank=True, max_length=90, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='about',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='activity_description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='ciiu',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='zone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Zone'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cellphone',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='ruc',
            field=models.CharField(blank=True, max_length=40, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(max_length=14, null=True),
        ),
    ]
