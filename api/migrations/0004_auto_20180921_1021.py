# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-21 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_bank_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='seller_asigned',
            new_name='seller_assigned',
        ),
        migrations.RenameField(
            model_name='sellercontact',
            old_name='email',
            new_name='email_exact',
        ),
        migrations.AddField(
            model_name='parameterseller',
            name='number_year',
            field=models.PositiveIntegerField(default=2018),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parameterseller',
            name='people_purchase_goal',
            field=models.PositiveIntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='queryplansacquired',
            name='queries_to_pay',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sellernonbillableplans',
            name='number_year',
            field=models.PositiveIntegerField(default=2018),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='agent_firstname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='agent_lastname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='business_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='commercial_reason',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='position',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='profession',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Unpaid'), (2, 'Progress'), (3, 'Paid')], default=1),
        ),
        migrations.AlterField(
            model_name='sellercontact',
            name='agent_firstname',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sellercontact',
            name='agent_lastname',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sellercontact',
            name='business_name',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sellercontact',
            name='commercial_reason',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sellercontact',
            name='first_name',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sellercontact',
            name='foreign_address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='sellercontact',
            name='last_name',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sellercontact',
            name='other_objection',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sellercontact',
            name='position',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sellercontact',
            name='profession',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
