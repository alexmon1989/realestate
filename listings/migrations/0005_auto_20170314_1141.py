# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 09:41
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_auto_20170303_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houseuserdata',
            name='repairs_maintenance',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Annual Repairs/Maintenance'),
        ),
    ]
