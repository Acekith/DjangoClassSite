# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-16 22:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu_item',
            name='truck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menuitems', to='website.Truck'),
        ),
    ]
