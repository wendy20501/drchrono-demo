# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-24 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.TextField()),
                ('duration', models.TextField()),
                ('exam_room', models.TextField()),
                ('office', models.TextField()),
                ('patient', models.TextField()),
                ('scheduled_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.TextField()),
            ],
        ),
    ]
