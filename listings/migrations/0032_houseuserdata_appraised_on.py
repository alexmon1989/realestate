# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-04 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0031_auto_20170523_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='houseuserdata',
            name='appraised_on',
            field=models.DateField(blank=True, null=True, verbose_name='Appraised on'),
        ),
    ]
