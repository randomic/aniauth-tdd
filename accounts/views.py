"""views for accounts app

"""
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.http import require_POST


def welcome_page(request):
    return render(request, 'accounts/welcome.html')


@require_POST
def send_login_email(request):
    email = EmailMultiAlternatives(
        'Your login link for ANIAuth',
        'To complete the login process, simply click on this link: ',
        to=[request.POST['email']]
    )
    email.send()
    return redirect(reverse_lazy('login_email_sent'))


def login_email_sent(request):
    return render(request, 'accounts/login_email_sent.html')
