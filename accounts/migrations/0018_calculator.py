# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 06:41
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0017_citiesconstants'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calculator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('managed', models.BooleanField(default=True, verbose_name='Managed')),
                ('property_managers_commission', models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(1)], verbose_name='Property Manager’s commission, %')),
                ('int_rate', models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(95), django.core.validators.MinValueValidator(5)], verbose_name='Int Rate, %')),
                ('deposit', models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(95), django.core.validators.MinValueValidator(5)], verbose_name='Deposit, %')),
                ('vacancy', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Vacancy, weeks')),
                ('capital_growth', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Capital Growth rate, %')),
                ('weekly_rent', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Weekly Rent, $')),
                ('purchase_price', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Purchase Price, $')),
                ('gross_yield', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)], verbose_name='Gross Yield, %')),
                ('net_yield', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)], verbose_name='Net Yield, %')),
                ('min_cashflow', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Min Cashflow, $')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.House')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]