from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from appointment.views import AppointmentViewSet
from patient.views import PatientViewSet
admin.autodiscover()

from . import views

router = DefaultRouter()
router.register(r'appointment', AppointmentViewSet)
router.register(r'patient', PatientViewSet)

urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorWelcome.as_view(), name='dashboard'),
    url(r'^checkin/$', views.PatientCheckIn.as_view(), name='checkin'),
    url(r'^admin/', admin.site.urls),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^api/', include((router.urls, 'api'), namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^waiting-chart/', views.PatientWaitingChart.as_view(), name='waiting'),
]