# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models

class Appointment(models.Model):
    doctor = models.TextField()
    duration = models.TextField()
    exam_room = models.TextField()
    office = models.TextField()
    patient = models.TextField()
    scheduled_time = models.DateTimeField(auto_now_add=True)
    status = models.TextField()

    class Meta:
        db_table = "appointment"