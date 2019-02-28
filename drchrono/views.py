from django.shortcuts import redirect
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth
from drchrono.endpoints import DoctorEndpoint
from drchrono.endpoints import AppointmentEndpoint
from drchrono.endpoints import PatientEndpoint
from appointment.models import Appointment
from doctor.models import Doctor
from patient.models import Patient
from datetime import date

class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    template_name = 'src/views/setup.html'

class DoctorWelcome(TemplateView):
    """
    The doctor can see what appointments they have today.
    """
    template_name = 'src/views/dashboard.html'

    def get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
        already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token

    def get_current_doctor(self, user):
        """
        Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've
        proved that the OAuth setup is working
        """
        access_token = self.get_token()
        api = DoctorEndpoint(access_token)
        doctor_data = next(api.list())
        Doctor.objects.update_or_create(
            defaults={'user': user, 'first_name': doctor_data['first_name'], 'last_name': doctor_data['last_name'],
                      'office_phone': doctor_data['office_phone']}, id=doctor_data['id'])

        return doctor_data

    def update_patients(self, doctor_id):
        access_token = self.get_token()
        api = PatientEndpoint(access_token)
        lst = list(api.list())
        for item in lst:
            Patient.objects.update_or_create(defaults={'doctor':Doctor(id=doctor_id), 'first_name':item['first_name'], 'last_name':item['last_name'], 'date_of_birth':item['date_of_birth'], 'gender':item['gender']}, id=item['id'])

    def update_appointments(self, doctor_id):
        access_token = self.get_token()
        api = AppointmentEndpoint(access_token)
        today = date.today()
        params = {}
        params['doctor'] = doctor_id
        lst = list(api.list(params=params,date=today))
        for item in lst:
            Appointment.objects.update_or_create(defaults={'doctor':Doctor(id=doctor_id), 'duration':item['duration'], 'exam_room':item['exam_room'], 'office':item['office'], 'patient':Patient(id=item['patient']), 'scheduled_time':item['scheduled_time'], 'status':item['status']}, id=item['id'])

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        doctor_details = self.get_current_doctor(kwargs['user'])
        kwargs['doctor'] = doctor_details
        self.update_patients(doctor_details['id'])
        self.update_appointments(doctor_details['id'])
        return kwargs

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            kwargs['user'] = request.user
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            return redirect('src/views/setup.html')

class PatientCheckIn(TemplateView):
    template_name = 'src/views/checkin.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            return redirect('src/views/setup.html')