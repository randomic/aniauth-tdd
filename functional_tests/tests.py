"""Functional tests for aniauth project

"""
from django.test import tag
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


@tag('functional')
class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def test_anon_redirected_to_welcome_page(self):
        """An unauthenticated user should be sent to the welcome page.

        """
        # They browse to this site.
        self.browser.get(self.live_server_url)
        # They see that this is a deployment of ANIAuth.
        self.assertIn('Welcome | ANIAuth', self.browser.title)
        # They are told to 'get started' by entering their email.
        self.fail('Finish test')
        # There is a form with one field for their email.
