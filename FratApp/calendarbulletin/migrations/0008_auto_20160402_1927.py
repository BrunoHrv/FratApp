# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 23:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('calendarbulletin', '0007_auto_20160402_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2016, 4, 12, 23, 27, 0, 914957, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='bulletinclearer',
            name='last_check',
            field=models.DateField(default=datetime.datetime(2016, 3, 23, 23, 27, 0, 914957, tzinfo=utc)),
        ),
    ]
