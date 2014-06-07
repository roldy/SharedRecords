from django.conf.urls import patterns, include, url

from rest_framework import routers
from facility import views



router = routers.DefaultRouter()
router.register(r'facility', views.FacilityViewSet)
router.register(r'personnel', views.PersonnelViewSet)
router.register(r'condition', views.ConditionViewSet)
router.register(r'patient', views.PatientViewSet)


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('facility.urls', namespace='facility')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), # rest_framework URLS
    url(r'^admin/', include(admin.site.urls)),
)
