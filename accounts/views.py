"""views for accounts app

"""
from django.shortcuts import render


def welcome_page(request):
    return render(request, 'accounts/welcome.html')
