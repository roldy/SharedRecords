from django.conf.urls import patterns, include, url
from facility import views


urlpatterns = patterns('',
            url(r'^$', views.index, name='index'),
            url(r'^login$', views.login_user, name='login'),
            url(r'^logout$', views.logout_user, name='logout_user'),
            url(r'^home/(?P<user_id>\d+)', views.home, name='home'),
            url(r'^search/$', views.search_page, name='search'),
            url(r'^dashboard/(?P<patient_id>\d+)/update', views.update_patient_data, name='update'),
           )
