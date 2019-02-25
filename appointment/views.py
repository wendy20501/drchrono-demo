# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from appointment.models import Appointment
from appointment.serializers import AppointmentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    #permission_classes = (IsAuthenticated,)