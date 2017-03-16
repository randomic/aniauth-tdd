"""views for accounts app

"""
from django.shortcuts import render
from django.views.decorators.http import require_POST


def welcome_page(request):
    return render(request, 'accounts/welcome.html')


@require_POST
def send_login_email(request):
    return render(request, 'accounts/login_email_sent.html')
