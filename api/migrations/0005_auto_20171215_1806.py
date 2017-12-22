# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-15 23:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20171212_1559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sellercontactnoefective',
            old_name='contact_bussinessname',
            new_name='business_name',
        ),
        migrations.RenameField(
            model_name='sellercontactnoefective',
            old_name='contact_firstname',
            new_name='commercial_reason',
        ),
        migrations.RenameField(
            model_name='sellercontactnoefective',
            old_name='contact_lastname',
            new_name='last_name',
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='about',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='activity_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Address'),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='birthdate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='cellphone',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='ciiu',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='civil_state',
            field=models.CharField(choices=[('c', 'cohabiting'), ('e', 'separated'), ('m', 'married'), ('w', 'widower'), ('d', 'divorced'), ('s', 'single')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='economic_sector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.EconomicSector'),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='email',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='first_name',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='institute',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='level_instruction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.LevelInstruction'),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='nationality',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='api.Countries'),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='ocupation',
            field=models.CharField(blank=True, choices=[('0', 'Employer'), ('1', 'Independent worker'), ('2', 'Employee'), ('3', 'Worker'), ('4', 'Worker in a family business'), ('5', 'Home worker'), ('6', 'Other')], max_length=1),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='photo',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='position',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='profession',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='ruc',
            field=models.CharField(max_length=40, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='sex',
            field=models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], max_length=1),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='telephone',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('0', 'pending'), ('1', 'activated'), ('2', 'rejected'), ('3', 'deactivated')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='address',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Department'),
        ),
        migrations.AlterField(
            model_name='address',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.District'),
        ),
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Province'),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='about',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='activity_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='ciiu',
            field=models.CharField(blank=True, default=1, max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='sex',
            field=models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seller',
            name='ciiu',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='sellercontactnoefective',
            name='document_number',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='sellercontactnoefective',
            name='latitude',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AlterField(
            model_name='sellercontactnoefective',
            name='longitude',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='anonymous',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='cellphone',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='user',
            name='document_number',
            field=models.CharField(max_length=45, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='document_type',
            field=models.CharField(choices=[('0', 'DNI'), ('1', 'Passport'), ('2', 'Foreign Card')], max_length=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_exact',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='img_document_number',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='nationality',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='api.Countries'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nick',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='residence_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='residence', to='api.Countries'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='api.Role'),
        ),
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
