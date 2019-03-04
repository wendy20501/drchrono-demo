# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_filters.rest_framework import DjangoFilterBackend
from drchrono.utility import FilterByDoctor
from patient.models import Patient
from patient.serializers import PatientSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = (DjangoFilterBackend, FilterByDoctor,)
    filter_fields = ('first_name', 'last_name', 'social_security_number')
    permission_classes = (IsAuthenticated,)