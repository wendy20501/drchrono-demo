# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    office_phone = models.CharField(max_length=35)

    class Meta:
        db_table = "doctor"