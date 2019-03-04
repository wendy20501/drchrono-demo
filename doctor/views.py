# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from doctor.models import Doctor
from doctor.serializers import DoctorSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = (IsAuthenticated,)
