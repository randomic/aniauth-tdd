"""aniauth accounts app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.views import LogoutView

import logintokens.views as views


urlpatterns = [
    url(r'^token_login/$', views.login,
        name='token_login'),
    url(r'^logout/$', LogoutView.as_view(),
        name='logout'),

    url(r'^send_token/$', views.send_login_email,
        name='send_token'),
    url(r'^send_token/done/$', views.login_email_sent,
        name='send_token_done'),
]
