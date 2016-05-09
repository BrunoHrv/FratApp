# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-09 01:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarbulletin', '0020_auto_20160501_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2016, 5, 18)),
        ),
        migrations.AlterField(
            model_name='bulletinclearer',
            name='last_check',
            field=models.DateField(default=datetime.date(2016, 4, 28)),
        ),
    ]
