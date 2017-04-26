"""views for accounts app

"""
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from logintokens.forms import LoginForm


@require_POST
def send_login_email(request):
    form = LoginForm(request.POST)

    if form.is_valid():
        form.save(request)
        return redirect(reverse_lazy('send_token_done'))
    else:
        return redirect(reverse_lazy('welcome'))


def login_email_sent(request):
    return render(request, 'accounts/login_email_sent.html')


def login(request):
    return render(request, 'accounts/login.html')
