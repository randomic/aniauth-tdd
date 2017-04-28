"""views for aniauth app

"""
from django.views.generic.base import TemplateView


class WelcomePageView(TemplateView):
    template_name = 'aniauth/welcome.html'
    title = 'Welcome'
