from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = "jobsauceapp"

urlpatterns = [
    path('', home, name='home'),
    path('jobs', job_list, name='jobs'),
    path('job/form', job_form, name='job_form'),
    path('jobs/<str:job_id>', job_details_form, name="job"),
    
    path('responses', response_list, name='responses'),
    path('response/form', response_form, name='response_form'),
    path('response/<str:response_id>', response_details_form, name='response'),
    # path('response/<str:response_id>/form', response_edit_form, name='response_edit_form'),
    # url(r'^books/(?P<book_id>[0-9]+)$', book_details, name="book"),
    # path('connections', social_connection_list, name='social_connection_list'),
    
    path('resources', resource_list, name='resources'),
    path('resource/form', resource_form, name='resource_form'),
    path('resource/<str:resource_id>', resource_detail_form, name='resource'),
    path('resource/<str:resource_id>/edit', resource_edit_form, name='edit'),

    url(r'accounts/', include('django.contrib.auth.urls')),
    path('logout', logout_user, name='logout'),
    path('register', register_user, name='register'),
]