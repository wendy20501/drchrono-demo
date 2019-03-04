from rest_framework import filters
from doctor.models import Doctor


class FilterByDoctor(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        doctor = Doctor.objects.get(user=request.user)
        return queryset.filter(doctor=doctor)