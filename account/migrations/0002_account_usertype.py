# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-22 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='usertype',
            field=models.IntegerField(choices=[(0, 'Regular'), (1, 'Owner')], default=1, help_text="If you own a food truck please select 'Owner'"),
            preserve_default=False,
        ),
    ]