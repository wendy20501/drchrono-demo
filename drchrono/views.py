from django.shortcuts import redirect
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth
from drchrono.endpoints import DoctorEndpoint
from drchrono.endpoints import AppointmentEndpoint
from drchrono.endpoints import PatientEndpoint
from appointment.models import Appointment
from doctor.models import Doctor
from patient.models import Patient
from datetime import date, timedelta
import json
import collections

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
        refresh_token = oauth_provider.extra_data['refresh_token']
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
            Patient.objects.update_or_create(defaults={'doctor':Doctor.objects.get(id=doctor_id), 'first_name':item['first_name'], 'last_name':item['last_name'], 'date_of_birth':item['date_of_birth'], 'gender':item['gender'], 'social_security_number':item['social_security_number']}, id=item['id'])

    def update_appointments(self, doctor_id):
        access_token = self.get_token()
        api = AppointmentEndpoint(access_token)
        today = date.today()
        params = {}
        params['doctor'] = doctor_id
        lst = list(api.list(params=params,date=today))
        for item in lst:
            Appointment.objects.update_or_create(defaults={'doctor':Doctor.objects.get(id=doctor_id), 'duration':item['duration'], 'exam_room':item['exam_room'], 'office':item['office'], 'patient':Patient.objects.get(id=item['patient']), 'scheduled_time':item['scheduled_time'], 'status':item['status']}, id=item['id'])

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        doctor_details = self.get_current_doctor(kwargs['user'])
        kwargs['doctor'] = doctor_details
        self.update_patients(doctor_details['id'])
        self.update_appointments(doctor_details['id'])
        return kwargs

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('setup')

        kwargs['user'] = request.user
        return super(DoctorWelcome, self).get(request, *args, **kwargs)

class PatientCheckIn(TemplateView):
    template_name = 'src/views/checkin.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('setup')

        return super(PatientCheckIn, self).get(request, *args, **kwargs)

class PatientWaitingChart(TemplateView):
    template_name = 'src/views/waitingChart.html'

    def get_day_avg_appt_wt(self, start):
        lst = Appointment.objects.filter(scheduled_time__date=start)
        tmp = [(x.session_time - x.checkin_time).seconds for x in lst if x.checkin_time is not None and x.session_time is not None]
        avg = sum(tmp)/(len(tmp)*60) if len(tmp) != 0 else 0
        return avg

    def get_context_data(self, **kwargs):
        kwargs = super(PatientWaitingChart, self).get_context_data(**kwargs)
        ret = {}
        for i in range(7):
            curDay = date.today() - timedelta(days=i)
            ret[str(curDay)] = self.get_day_avg_appt_wt(curDay)

        kwargs['avg_wait_time'] = json.dumps(collections.OrderedDict(sorted(ret.items())))
        return kwargs

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('setup')

        return super(PatientWaitingChart, self).get(request, *args, **kwargs)