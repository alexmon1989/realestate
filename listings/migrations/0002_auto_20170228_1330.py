# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='markedhouse',
            name='mark',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='listings.Mark'),
        ),
    ]
