# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from appointment.models import Appointment

admin.site.register(Appointment)