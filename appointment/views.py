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

from patient.models import Patient


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    #permission_classes = (IsAuthenticated,)

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

        def update_server(request, pk):
            access_token = get_token()
            api = AppointmentEndpoint(access_token)
            api.update(pk, data=json.loads(request.body), partial=True)

        update_server(request, pk)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)