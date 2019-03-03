# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework.utils import json
from social_django.models import UserSocialAuth

from appointment.models import Appointment
from appointment.serializers import AppointmentSerializer
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from doctor.models import Doctor
from drchrono.endpoints import AppointmentEndpoint
from datetime import datetime
from dateutil.parser import parse
#from drchrono.utility import FilterByDoctor

from patient.models import Patient

class FilterByDoctor(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        print('########', request.user)
        doctor = Doctor.objects.get(user=request.user)
        return queryset.filter(doctor=doctor)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    print('hello')
    filter_backends = (FilterByDoctor,)
    permission_classes = (IsAuthenticated,)
    # filter_fields = ("patient",)

    def queryTest(self, myDict):
        ret = self.get_queryset().filter(**myDict)
        serializer = AppointmentSerializer(instance=ret, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def search_today_appt(self, request):
        return self.queryTest({'scheduled_time__date': datetime.today()})

    @action(methods=['get'], detail=False)
    def search_related_appt(self, request, pk=None):
        patient_id = request.GET.get("patient_id")
        query_date = parse(request.GET.get("date"))
        return self.queryTest({'patient_id': patient_id, 'scheduled_time__date': query_date})


    def partial_update(self, request, *args, **kwargs):
        def get_token():
            oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
            access_token = oauth_provider.extra_data['access_token']
            return access_token

        def update_server(request, *args, **kwargs):
            access_token = get_token()
            api = AppointmentEndpoint(access_token)
            param = request.data
            param['checkin_time'] = datetime.datetime.now()
            print(param)
            api.update(kwargs['pk'], param)

        update_server(request, *args, **kwargs)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)