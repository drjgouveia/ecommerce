from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse


@login_required(login_url="auth/login")
def homepage(request):
    return render(request, 'homepage.html')
