# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-13 11:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_vhousesfortables'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'managed': False, 'ordering': ('city_name',), 'verbose_name': 'City', 'verbose_name_plural': 'Cities'},
        ),
    ]
