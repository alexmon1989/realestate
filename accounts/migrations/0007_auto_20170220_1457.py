# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 12:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20170220_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='housesfilter',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='housesfilter',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
