# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_profile_font_ratio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='font_ratio',
            field=models.FloatField(default=1, verbose_name='Font size'),
        ),
    ]