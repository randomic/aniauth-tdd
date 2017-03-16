"""views for accounts app

"""
from django.shortcuts import render


def welcome_page(request):
    return render(request, 'accounts/welcome.html')


def send_login_email(request):
    return render(request, 'accounts/login_email_sent.html')
