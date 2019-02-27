from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from appointment.views import AppointmentViewSet
admin.autodiscover()

from . import views

router = DefaultRouter()
router.register(r'appointment', AppointmentViewSet)

urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorWelcome.as_view(), name='setup'),
    url(r'^checkin/$', views.PatientCheckIn.as_view(), name='checkin'),
    url(r'^admin/', admin.site.urls),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    #url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^api/', include((router.urls, 'api'), namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]