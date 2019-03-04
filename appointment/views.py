# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from social_django.models import UserSocialAuth
from django_filters.rest_framework import DjangoFilterBackend
from appointment.models import Appointment
from appointment.serializers import AppointmentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drchrono.endpoints import AppointmentEndpoint
from datetime import datetime
from drchrono.utility import FilterByDoctor

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

    def partial_update(self, request, *args, **kwargs):
        def get_token():
            oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
            access_token = oauth_provider.extra_data['access_token']
            return access_token

        def update_server(request, *args, **kwargs):
            # Update DrChrono DB
            access_token = get_token()
            api = AppointmentEndpoint(access_token)
            param = request.data
            api.update(kwargs['pk'], param)

            # Update local DB
            if "status" in param:
                if param["status"] == "Checked In":
                    param['checkin_time'] = datetime.now()
                elif param["status"] == "In Session":
                    param['session_time'] = datetime.now()

        update_server(request, *args, **kwargs)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)