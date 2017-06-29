# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-23 09:01
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0030_auto_20170424_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houseuserdata',
            name='insurance',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Insurance *'),
        ),
        migrations.AlterField(
            model_name='houseuserdata',
            name='market_reg_value',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Market/reg value *'),
        ),
        migrations.AlterField(
            model_name='houseuserdata',
            name='offer_price',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Offer price *'),
        ),
        migrations.AlterField(
            model_name='houseuserdata',
            name='rates',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Council Rates *'),
        ),
        migrations.AlterField(
            model_name='houseuserdata',
            name='rent_per_week',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Rent per week *'),
        ),
        migrations.AlterField(
            model_name='houseuserdata',
            name='repairs_maintenance',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Annual Repairs/Maintenance *'),
        ),
    ]