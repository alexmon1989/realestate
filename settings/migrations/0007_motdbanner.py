# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-05 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_auto_20170507_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotdBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=False, verbose_name='Enabled')),
                ('message', models.CharField(default='It will be tachnical work on the site soon.', max_length=255, verbose_name='Message')),
            ],
            options={
                'verbose_name_plural': 'MOTD banner',
                'verbose_name': 'MOTD banner',
            },
        ),
    ]