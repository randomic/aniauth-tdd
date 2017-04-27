"""Functional tests for aniauth project

"""
import re

from django.test import tag
from django.core import mail
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10
TEST_EMAIL = 'newvisitor@example.com'


@tag('functional')
class NewVisitorTest(StaticLiveServerTestCase):
    """Tests for first-time users visiting the site.

    """
    @classmethod
    def setUpClass(cls):
        super(NewVisitorTest, cls).setUpClass()
        cls.browser = webdriver.Chrome()
        cls.browser.maximize_window()
        cls.browser.implicitly_wait(MAX_WAIT)
        super(NewVisitorTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.refresh()
        cls.browser.refresh()
        cls.browser.quit()
        super(NewVisitorTest, cls).tearDownClass()

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

        self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text)

        # Their email contains a message from ANIAuth.
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertIn('Your login link for ANIAuth', email.subject)

        # The email contains a url link.
        url_search = re.search(r'https?://.+/.+$', email.body)
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # The url is clicked.
        self.browser.get(url)

        # The user is logged in.
        self.assertIn(
            'Logout',
            self.browser.find_element_by_tag_name('nav').text)

        self.browser.refresh()
