# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-20 16:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0025_otherexpenses'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OtherExpenses',
            new_name='OtherExpense',
        ),
    ]
