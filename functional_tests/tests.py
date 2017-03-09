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

    def test_anon_sees_welcome_page(self):
        """An unauthenticated user should be able to see the welcome page.

        """
        # They browse to this site.
        self.browser.get(self.live_server_url)
        # They see that this is a deployment of ANIAuth.
        self.assertIn('Welcome | ANIAuth', self.browser.title)
        # They are told to 'get started' by entering their email.
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('get started', body)
        self.assertIn('enter your email address below', body)
        # There is a form with one field for their email.
        self.fail('Finish test')
