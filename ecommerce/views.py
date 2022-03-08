from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from sells.models import Sell
from prods.models import Product


@login_required(login_url="auth/login")
def homepage(request):
    """
    Loads data for the homepage

    :param request: user request
    :return: returns the page with the rendered information
    """
    prods = Product.objects.all()
    sells = Sell.objects.all()
    return render(request, 'homepage.html', {"prods": prods, "sells": sells})
