# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-26 01:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_supply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supply',
            name='owners',
        ),
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
