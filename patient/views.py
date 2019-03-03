# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
#from drchrono.utility import FilterByDoctor
from patient.models import Patient
from patient.serializers import PatientSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    #filter_backends = (FilterByDoctor,)
    filter_fields = ('first_name', 'last_name')
    #permission_classes = (IsAuthenticated,)

    # @action(methods=['get'], detail=False)
    # def search_patient_by_query(self, request, pk=None):
    #     first_name = self.request.GET['first_name']
    #     last_name = self.request.GET['last_name']
    #     patients = self.get_queryset().filter(first_name=first_name, last_name=last_name)
    #     serializer = PatientSerializer(instance=patients, many=True)
    #     return Response(serializer.data)