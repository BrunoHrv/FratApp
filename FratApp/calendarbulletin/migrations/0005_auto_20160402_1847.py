# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 22:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('calendarbulletin', '0004_auto_20160402_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='expiration_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='postDate',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='bulletinclearer',
            name='last_check',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]