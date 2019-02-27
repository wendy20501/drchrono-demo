from django.shortcuts import redirect
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth
from drchrono.endpoints import DoctorEndpoint
from drchrono.endpoints import AppointmentEndpoint
from appointment.models import Appointment
from datetime import date

class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    template_name = 'src/views/setup.html'
    #template_name = 'index.html'  # type: str

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

    def make_api_request(self):
        """
        Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've
        proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use it to fetch details
        access_token = self.get_token()
        api = DoctorEndpoint(access_token)
        # Grab the first doctor from the list; normally this would be the whole practice group, but your hackathon
        # account probably only has one doctor in it.
        return next(api.list())

    def update_appointments(self, doctor):
        access_token = self.get_token()
        api = AppointmentEndpoint(access_token)
        today = date.today()
        params = {}
        params['doctor'] = doctor
        lst = list(api.list(params=params,date=today))
        for item in lst:
            obj, created = Appointment.objects.update_or_create(defaults={'doctor':item['doctor'], 'duration':item['duration'], 'exam_room':item['exam_room'], 'office':item['office'], 'patient':item['patient'], 'scheduled_time':item['scheduled_time'], 'status':item['status']}, id=item['id'])

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        doctor_details = self.make_api_request()
        kwargs['doctor'] = doctor_details
        self.update_appointments(doctor_details['id'])
        return kwargs

class PatientCheckIn(TemplateView):
    template_name = 'src/views/checkin.html'
