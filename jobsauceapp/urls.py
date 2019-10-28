from django.conf.urls import url
from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = "jobsauceapp"

urlpatterns = [
    path('jobs', job_list, name='list'),
    # path('job/form', job_form, name='job_form'),
    # path('responses', response_list, name='response_list'),
    # path('response/form', response_form, name='response_form'),
    # path('connections', social_connection_list, name='social_connection_list'),
    # path('resources', study_resource_list, name='study_resource_list'),
    # path('resource/form', study_resource_form, name='study_resource_form'),

    url(r'accounts/', include('django.contrib.auth.urls')),
    # url(r'^logout/$', logout_user, name='logout'),
    # url(r'^register/$', register_user, name='register'),
]