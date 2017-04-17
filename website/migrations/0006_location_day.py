# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-17 01:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='day',
            field=models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], default=6),
            preserve_default=False,
        ),
    ]