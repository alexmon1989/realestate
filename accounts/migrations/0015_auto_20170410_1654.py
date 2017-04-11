# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 13:54
from __future__ import unicode_literals

import annoying.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_constants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constants',
            name='inflation',
            field=models.FloatField(default=1, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)], verbose_name='Inflation, %'),
        ),
        migrations.AlterField(
            model_name='constants',
            name='loan_deposit',
            field=models.FloatField(default=5, validators=[django.core.validators.MaxValueValidator(95), django.core.validators.MinValueValidator(5)], verbose_name='Loan deposit, %'),
        ),
        migrations.AlterField(
            model_name='constants',
            name='loan_interest_rate',
            field=models.FloatField(default=5, validators=[django.core.validators.MaxValueValidator(95), django.core.validators.MinValueValidator(5)], verbose_name='Loan interest rate, %'),
        ),
        migrations.AlterField(
            model_name='constants',
            name='min_cashflow',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Min cashflow'),
        ),
        migrations.AlterField(
            model_name='constants',
            name='net_yield',
            field=models.FloatField(default=1, validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)], verbose_name='Net yield, %'),
        ),
        migrations.AlterField(
            model_name='constants',
            name='new_built_loan_deposit',
            field=models.FloatField(default=5, validators=[django.core.validators.MaxValueValidator(95), django.core.validators.MinValueValidator(5)], verbose_name='New-build loan deposit, %'),
        ),
        migrations.AlterField(
            model_name='constants',
            name='property_management_commission',
            field=models.FloatField(default=1, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(1)], verbose_name='Property Management commission, %'),
        ),
        migrations.AlterField(
            model_name='constants',
            name='user',
            field=annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='constants',
            name='vacancy_rate',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Vacancy rate, weeks'),
        ),
    ]
