# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-12 20:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20171206_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='foreign_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='ciiu',
            field=models.CharField(blank=True, default=1211, max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Address', verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='anonymous',
            field=models.BooleanField(default=True, verbose_name='anonymous'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cellphone',
            field=models.CharField(blank=True, max_length=14, verbose_name='cellphone'),
        ),
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.CharField(max_length=45, unique=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='user',
            name='document_number',
            field=models.CharField(max_length=45, unique=True, verbose_name='document number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='document_type',
            field=models.CharField(choices=[('0', 'DNI'), ('1', 'Passport'), ('2', 'Foreign Card')], max_length=1, verbose_name='document type'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_exact',
            field=models.CharField(max_length=150, unique=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='img_document_number',
            field=models.CharField(max_length=250, null=True, verbose_name='upload document'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nationality',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='api.Countries', verbose_name='nacionalidad'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nick',
            field=models.CharField(blank=True, max_length=45, verbose_name='nick'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.CharField(max_length=250, null=True, verbose_name='photo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='residence_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='residence', to='api.Countries', verbose_name='residence country'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='api.Role', verbose_name='role'),
        ),
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(blank=True, max_length=14, verbose_name='telephone'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='updated at'),
        ),
    ]