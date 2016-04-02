# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 22:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarbulletin', '0002_auto_20160402_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 12, 18, 33, 2, 43564)),
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='postDate',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 2, 18, 33, 2, 43564), editable=False),
        ),
        migrations.AlterField(
            model_name='bulletinclearer',
            name='last_check',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 2, 18, 33, 2, 43564)),
        ),
    ]
