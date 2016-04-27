# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-27 16:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarbulletin', '0016_auto_20160425_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2016, 5, 7)),
        ),
        migrations.AlterField(
            model_name='bulletinclearer',
            name='last_check',
            field=models.DateField(default=datetime.date(2016, 4, 17)),
        ),
    ]
