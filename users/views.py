from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegisterForm


def user_login(request):
    """
    View used to login the user into the app

    :param request: request made with username and password
    :return: if successful will redirect to the homepage, else will either return an error in the login apge or will return the login page
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return render(request, 'auth/login.html',
                          {'error_message': 'Incorrect username and / or password.'})
    else:
        logout(request)
        return render(request, 'auth/login.html')


@login_required(login_url="auth/login")
def user_logout(request):
    """
    View responsible for logging out the user

    :param request: request made by the user with its information
    :return: if successful will redirect to the login page
    """

    logout(request)
    return HttpResponseRedirect(reverse('login'))


def user_register(request):
    """
    This view is responsible to register the user into the database.

    :param request: request with the data filled from the form
    :return: will return error and redirect to the registeer page if the user has already been created, passwords don't
                match or email already exists, or will just return the register page. Else will redirect to the homepage.
    """
    template = 'auth/register.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords don\'t match.'
                })
            else:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()

                login(request, user)

                return HttpResponseRedirect(reverse('homepage'))

    else:
        logout(request)
        form = RegisterForm()

    return render(request, template, {'form': form})
