# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-03-03 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_auto_20190301_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='waiting_time',
            field=models.DateTimeField(null=True),
        ),
    ]
