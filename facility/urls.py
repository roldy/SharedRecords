from django.conf.urls import patterns, include, url
from facility import views

urlpatterns = patterns('',
            url(r'^$', views.index, name='index'),
            url(r'^login$', views.login_user, name='login'),
            url(r'^logout$', views.logout_user, name='logout_user'),
            url(r'^home/(?P<user_id>\d+)', views.home, name='home'),
            url(r'^search/$', views.search_page, name='search'),
            url(r'^condition/$', views.add_condition, name='condition'),
            url(r'^patient/add/$', views.add_patient, name='add_patient'),
            url(r'^other/condition/(?P<patient_id>\d+)$', views.add_patient_data_from_alternate_facility, name='other_condition'),
            url(r'^dashboard/(?P<patient_id>\d+)/update', views.update_patient_data, name='update'),
            url(r'^dashboard/(?P<patient_id>\d+)/details', views.patient_details, name='details'),
           )
