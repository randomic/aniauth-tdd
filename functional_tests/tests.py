"""Functional tests for aniauth project

"""
import re
import time

from django.test import tag
from django.core import mail
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 10
TEST_EMAIL = 'newvisitor@example.com'


@tag('functional')
class NewVisitorTest(StaticLiveServerTestCase):
    """Tests for first-time users visiting the site.

    """
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def wait_for(self, func):
        """Waits for up to MAX_WAIT seconds for an assertation to pass.

        """
        start_time = time.time()
        while True:
            try:
                return func()
            except (AssertionError, WebDriverException) as exc:
                if time.time() - start_time > MAX_WAIT:
                    raise exc
                time.sleep(0.5)

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
        self.assertIn('enter your email address', body)
        # There is a form with one field for their email.
        emailinput = self.browser.find_element_by_id('id_email')
        self.assertEqual(emailinput.get_attribute('placeholder'),
                         'Email')

    def test_anon_can_login_with_email(self):
        """A new user should be able to login with only their email address.

        """
        # They browse to this site.
        self.browser.get(self.live_server_url)
        # They enter their email address into the input box.
        emailinput = self.browser.find_element_by_name('email')
        emailinput.send_keys(TEST_EMAIL)
        emailinput.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Their email contains a message from ANIAuth.
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertIn('Your login link for ANIAuth', email.subject)

        # The email contains a url link.
        url_search = re.search(r'http://.+/.+$', email.body)
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # The url is clicked.
        self.browser.get(url)

        # The user is logged in.
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Logout')
        )
