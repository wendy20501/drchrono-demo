# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from doctor.models import Doctor
from patient.models import Patient

class Appointment(models.Model):
    STATUS_CHOICE = (
        ("", ""),
        ("Checked In", "Checked In"),
        ("In Session", "In Session"),
        ("Complete", "Complete"),
        ("Cancelled", "Cancelled"),
    )
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    duration = models.IntegerField()
    exam_room = models.CharField(max_length=20)
    office = models.CharField(max_length=20)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField(auto_now_add=True)
    checkin_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, null=True, choices=STATUS_CHOICE, default="")
    session_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "appointment"