# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-21 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travels_app', '0005_auto_20180518_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='trip_creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_trips', to='travels_app.User'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='users',
            field=models.ManyToManyField(related_name='trips', to='travels_app.User'),
        ),
    ]
