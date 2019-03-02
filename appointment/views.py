# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework.utils import json
from social_django.models import UserSocialAuth

from appointment.models import Appointment
from appointment.serializers import AppointmentSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drchrono.endpoints import AppointmentEndpoint
import datetime
from datetime import date

from patient.models import Patient


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    #permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=False)
    def search_today_appt(self, request, pk=None):
        appointments = self.get_queryset().filter(scheduled_time__date=date.today())
        serializer = AppointmentSerializer(instance=appointments, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def search_related_appt(self, request, pk=None):
        patient_id = request.GET.get("patient_id")
        appointments = self.get_queryset().filter(patient_id=patient_id)
        serializer = AppointmentSerializer(instance=appointments, many=True)
        return Response(serializer.data)

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