# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from patient.models import Patient
from patient.serializers import PatientSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    #permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        first_name = self.request.GET['first_name']
        last_name = self.request.GET['last_name']

        return self.queryset.filter({'first_name':first_name, 'last_name':last_name})
