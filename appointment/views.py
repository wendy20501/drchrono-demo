# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework.utils import json
from social_django.models import UserSocialAuth
from django_filters.rest_framework import DjangoFilterBackend
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
from drchrono.utility import FilterByDoctor

from patient.models import Patient


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = (DjangoFilterBackend, FilterByDoctor,)
    permission_classes = (IsAuthenticated,)
    filter_fields = ("patient",)

    def get_queryset(self):
        queryset = super(AppointmentViewSet, self).get_queryset()

        date = self.request.GET.get("date")
        if date:
            year, month, day = date.split("-")
            return queryset.filter(
                scheduled_time__year=year,
                scheduled_time__month=month,
                scheduled_time__day=day,
            )
        return queryset

    def queryTest(self, myDict):
        ret = self.get_queryset().filter(**myDict)
        serializer = AppointmentSerializer(instance=ret, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def search_today_appt(self, request):
        return self.queryTest({'scheduled_time__date': datetime.today()})

    @action(methods=['get'], detail=False)
    def search_related_appt(self, request):
        patient = request.GET.get("patient")
        query_date = parse(request.GET.get("date"))
        return self.queryTest({'patient':patient,'scheduled_time__date': query_date})

    def partial_update(self, request, *args, **kwargs):
        def get_token():
            oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
            access_token = oauth_provider.extra_data['access_token']
            return access_token

        def update_server(request, *args, **kwargs):
            access_token = get_token()
            api = AppointmentEndpoint(access_token)
            param = request.data
            if "status" in param:
                if param["status"] == "Checked In":
                    param['checkin_time'] = datetime.now()
                elif param["status"] == "In Session":
                    param['session_time'] = datetime.now()
            api.update(kwargs['pk'], param)

        update_server(request, *args, **kwargs)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)