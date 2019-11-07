from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import login

def login_user(request):
    login(request)
    return redirect(reverse('jobsauceapp:home'))