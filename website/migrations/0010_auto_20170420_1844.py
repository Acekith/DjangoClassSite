# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 23:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20170418_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='end_time',
            field=models.TimeField(help_text='Please use 24hr format: HH:MM:SS'),
        ),
        migrations.AlterField(
            model_name='location',
            name='start_time',
            field=models.TimeField(help_text='Please use 24hr format: HH:MM:SS'),
        ),
    ]
