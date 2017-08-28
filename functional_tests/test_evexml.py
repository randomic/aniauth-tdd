"""Functional tests for the xml api part of aniauth project.

This is a temporary app as EVE Online's xml api is deprecated and will be
disabled March 2018.

"""
import json

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from django.shortcuts import reverse
from django.conf import settings
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

        data_dir = getattr(settings, 'DATA_DIR')
        with data_dir.joinpath('conf', 'test_secrets.json').open() as handle:
            secrets = json.load(handle)
            cls.testkeys = secrets['apikeys']

    @classmethod
    def tearDownClass(cls):
        cls.browser.refresh()
        cls.browser.quit()
        super(SubmissionTest, cls).tearDownClass()

    def tearDown(self):
        self.browser.refresh()

    def test_user_submits_valid_key(self):
        """Expected behaviour for user submitting valid API Keypair.

        """
        # They browse to the eve api keys page.
        url = self.live_server_url + reverse('eveapi_add')
        self.browser.get(url)
        # They see input boxes for key_id and v_code.
        key_id_input = self.browser.find_element_by_name('key_id')
        self.assertEqual(key_id_input.get_attribute('placeholder'), 'keyID')
        v_code_input = self.browser.find_element_by_name('v_code')
        self.assertEqual(v_code_input.get_attribute('placeholder'), 'vCode')

        valid_key = self.testkeys['full']['all']
        key_id_input.send_keys(valid_key['key_id'])
        v_code_input.send_keys(valid_key['v_code'])
        v_code_input.send_keys(Keys.ENTER)

        self.assertIn(
            'Your API key has been successfully saved',
            self.browser.find_element_by_tag_name('body').text)
