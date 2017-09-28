# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 16:52
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nick', models.CharField(blank=True, max_length=45)),
                ('email_exact', models.CharField(max_length=150, unique=True)),
                ('telephone', models.CharField(max_length=14)),
                ('cellphone', models.CharField(max_length=14)),
                ('photo', models.CharField(default='preview.png', max_length=250)),
                ('document_type', models.CharField(choices=[('0', 'DNI'), ('1', 'Passport'), ('2', 'Foreign Card')], max_length=1)),
                ('document_number', models.CharField(max_length=45, unique=True)),
                ('ruc', models.CharField(max_length=40, null=True, unique=True)),
                ('code', models.CharField(max_length=45, unique=True)),
                ('anonymous', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=155)),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AlertCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('c', 'Critic'), ('m', 'Moderate'), ('p', 'Positive')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('calification', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, unique=True)),
                ('image', models.CharField(max_length=169)),
                ('description', models.CharField(max_length=255)),
                ('payment_per_answer', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CommercialGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='ContractCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_file', models.CharField(max_length=50)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90, unique=True)),
                ('code_phone', models.CharField(max_length=4, unique=True)),
                ('iso_code', models.CharField(max_length=4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_card', models.CharField(max_length=16)),
                ('cvc', models.CharField(max_length=4)),
                ('expiration_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CulqiPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('culqi_code', models.CharField(max_length=40)),
                ('status', models.CharField(choices=[('w', 'Wait'), ('d', 'Denied'), ('e', 'Exhaled'), ('p', 'Paid')], max_length=1)),
                ('credit_cartd', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.CreditCard')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='EconomicSector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.CharField(max_length=20)),
                ('fee_order_number', models.PositiveIntegerField()),
                ('fee_amount', models.FloatField()),
                ('transaction_code', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='FeeNextMonthSeller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_promotion', models.PositiveIntegerField()),
                ('fee_contacts', models.PositiveIntegerField()),
                ('fee_products', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LevelInstruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Objection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65)),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter', models.CharField(max_length=45)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('api_client', models.TextField(null=True)),
                ('tablename', models.CharField(max_length=17, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=220)),
                ('code', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('query_amount', models.IntegerField()),
                ('expiration_number', models.PositiveIntegerField()),
                ('price', models.FloatField()),
                ('is_active', models.BooleanField()),
                ('created_at', models.DateTimeField()),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Plan')),
            ],
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=45)),
                ('discount', models.FloatField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('type_discount', models.CharField(choices=[('p', 'Percentage'), ('n', 'Number')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.FloatField()),
                ('reference_number', models.CharField(max_length=30)),
                ('fee_number', models.PositiveIntegerField()),
                ('latitude', models.CharField(max_length=45, null=True)),
                ('longitude', models.CharField(max_length=45, null=True)),
                ('query_available', models.PositiveIntegerField()),
                ('is_promotional', models.BooleanField()),
                ('last_number_fee_paid', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('0', 'Pending'), ('1', 'Paid')], max_length=1)),
                ('expiration_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Product')),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.Promotion')),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('has_precedent', models.BooleanField()),
                ('status', models.CharField(choices=[('0', 'Pending'), ('1', 'Accepted'), ('2', 'Declined'), ('3', 'Answered')], max_length=1)),
                ('declined_motive', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='QueryAnswerFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100)),
                ('type_file', models.CharField(choices=[('0', 'Image'), ('1', 'Voice'), ('2', 'Document')], max_length=1)),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('permissions', models.ManyToManyField(db_table='role_permission', to='dashboard.Permmission')),
            ],
        ),
        migrations.CreateModel(
            name='SellerContactNoEfective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_firstname', models.CharField(max_length=45, null=True)),
                ('contact_lastname', models.CharField(max_length=55, null=True)),
                ('type_contact', models.CharField(choices=[('n', 'Natural'), ('b', 'Bussiness')], max_length=1)),
                ('document_type', models.CharField(choices=[('0', 'DNI'), ('1', 'Passport'), ('2', 'Foreign Card')], max_length=1)),
                ('document_number', models.CharField(max_length=18)),
                ('contact_bussinessname', models.CharField(max_length=45, null=True)),
                ('agent_firstname', models.CharField(max_length=45, null=True)),
                ('agent_lastname', models.CharField(max_length=45, null=True)),
                ('latitude', models.CharField(max_length=45)),
                ('longitude', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('objection', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Objection')),
            ],
        ),
        migrations.CreateModel(
            name='SpecialistContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_case', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('r', 'Requested'), ('a', 'Accepted'), ('d', 'Declined')], max_length=1)),
                ('declined_motive', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('short_description', models.CharField(max_length=25)),
                ('long_description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('districts', models.ManyToManyField(db_table='zones_districts', to='dashboard.District')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('type_client', models.CharField(choices=[('n', 'Natural'), ('b', 'Bussiness')], max_length=1)),
                ('sex', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1, null=True)),
                ('civil_state', models.CharField(choices=[('s', 'Single'), ('m', 'Married'), ('d', 'Divorce'), ('w', 'Widower')], max_length=1, null=True)),
                ('birthdate', models.DateField(null=True)),
                ('ciiu', models.CharField(max_length=4)),
                ('activity_description', models.CharField(max_length=255)),
                ('institute', models.CharField(blank=True, max_length=100, null=True)),
                ('ocupation', models.CharField(choices=[('d', 'Dependent'), ('i', 'Independent')], max_length=1)),
                ('about', models.CharField(max_length=255)),
                ('bussiness_name', models.CharField(max_length=45, null=True)),
                ('agent_firstname', models.CharField(max_length=45, null=True)),
                ('agent_lastname', models.CharField(max_length=45, null=True)),
                ('position', models.CharField(max_length=45, null=True)),
                ('commercial_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.CommercialGroup')),
                ('economic_sector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.EconomicSector')),
                ('level_instruction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.LevelInstruction')),
                ('profession', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.Profession')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
            bases=('dashboard.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='QueryLog',
            fields=[
                ('query_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.Query')),
                ('actions', models.CharField(max_length=10)),
                ('changed_on', models.DateTimeField()),
            ],
            bases=('dashboard.query',),
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('cv', models.CharField(blank=True, max_length=100, null=True)),
                ('monthly_fee_plans', models.PositiveIntegerField()),
                ('monthly_fee_contacts', models.PositiveIntegerField()),
                ('monthly_promotional_plans', models.PositiveIntegerField()),
                ('count_month_promotional', models.PositiveIntegerField()),
                ('count_month_plans', models.PositiveIntegerField()),
                ('count_month_contacts', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Zone')),
            ],
            options={
                'verbose_name': 'Seller',
                'verbose_name_plural': 'Sellers',
            },
            bases=('dashboard.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bussiness_name', models.CharField(max_length=55)),
                ('type_specialist', models.CharField(choices=[('m', 'Main'), ('a', 'Associate')], max_length=1)),
                ('star_rating', models.IntegerField(null=True)),
                ('cv', models.CharField(max_length=150)),
                ('payment_per_answer', models.FloatField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Category')),
            ],
            options={
                'verbose_name': 'Specialist',
                'verbose_name_plural': 'Specialists',
            },
            bases=('dashboard.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='queryanswerfiles',
            name='query',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.Query'),
        ),
        migrations.AddField(
            model_name='query',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Category'),
        ),
        migrations.AddField(
            model_name='query',
            name='precedent',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.Query'),
        ),
        migrations.AddField(
            model_name='fee',
            name='payment_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.PaymentType'),
        ),
        migrations.AddField(
            model_name='fee',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Purchase'),
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Province'),
        ),
        migrations.AddField(
            model_name='answer',
            name='query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Query'),
        ),
        migrations.AddField(
            model_name='alertcategory',
            name='interval',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Interval'),
        ),
        migrations.AddField(
            model_name='alert',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.AlertCategory'),
        ),
        migrations.AddField(
            model_name='alert',
            name='role',
            field=models.ManyToManyField(db_table='role_alert', to='dashboard.Role'),
        ),
        migrations.AddField(
            model_name='address',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Department'),
        ),
        migrations.AddField(
            model_name='address',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.District'),
        ),
        migrations.AddField(
            model_name='address',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Province'),
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.Address'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='nationality',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='dashboard.Countries'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='dashboard.Role'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='specialistcontract',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Client'),
        ),
        migrations.AddField(
            model_name='specialistcontract',
            name='specialist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Specialist'),
        ),
        migrations.AddField(
            model_name='sellercontactnoefective',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Seller'),
        ),
        migrations.AddField(
            model_name='query',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Client'),
        ),
        migrations.AddField(
            model_name='query',
            name='specialist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Specialist'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Client'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.Seller'),
        ),
        migrations.AddField(
            model_name='creditcard',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Client'),
        ),
        migrations.AddField(
            model_name='answer',
            name='specialist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.Specialist'),
        ),
    ]
