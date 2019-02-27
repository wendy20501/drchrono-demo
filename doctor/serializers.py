from rest_framework import serializers
from appointment.models import Appointment
from doctor.models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'