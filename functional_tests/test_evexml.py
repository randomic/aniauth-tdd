"""Functional tests for the xml api part of aniauth project.

This is a temporary app as EVE Online's xml api is deprecated and will be
disabled March 2018.

"""
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from django.shortcuts import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10


@tag('functional')
class SubmissionTest(StaticLiveServerTestCase):
    """Tests for users who are submitting xml api key.

    """
    @classmethod
    def setUpClass(cls):
        super(SubmissionTest, cls).setUpClass()
        cls.browser = webdriver.Chrome()
        cls.browser.maximize_window()
        cls.browser.implicitly_wait(MAX_WAIT)

    @classmethod
    def tearDownClass(cls):
        cls.browser.refresh()
        cls.browser.quit()
        super(SubmissionTest, cls).tearDownClass()

    def tearDown(self):
        self.browser.refresh()

    def test_user_can_see_apikey_form(self):
        """A user should be able to see the form for submitting api keys.

        """
        # They browse to the eve api keys page.
        url = self.live_server_url + reverse('eveapi_add')
        self.browser.get(url)
        # They see input boxes for key_id and v_code.
        key_id_input = self.browser.find_element_by_name('key_id')
        v_code_input = self.browser.find_element_by_name('v_code')
