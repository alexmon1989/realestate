# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-12 06:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20170410_1526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='global',
            options={'verbose_name': 'Global constants', 'verbose_name_plural': 'Global constants'},
        ),
    ]
