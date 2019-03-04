from __future__ import unicode_literals

from django.db import models
from doctor.models import Doctor

# Create your models here.
class Patient(models.Model):
    GENDER_CHOICE = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    date_of_birth = models.DateTimeField(null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, default="Male")
    social_security_number = models.CharField(null=True, max_length=9)

    class Meta:
        db_table = "patient"