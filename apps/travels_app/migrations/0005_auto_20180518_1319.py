# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-18 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels_app', '0004_trip_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='users',
            field=models.ManyToManyField(null=True, related_name='trips', to='travels_app.User'),
        ),
    ]