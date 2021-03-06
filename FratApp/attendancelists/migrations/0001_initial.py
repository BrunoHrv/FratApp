# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-06 19:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creator', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField(max_length=200)),
                ('postDate', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-postDate'],
            },
        ),
        migrations.AddField(
            model_name='attendee',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendancelists.Event'),
        ),
    ]
