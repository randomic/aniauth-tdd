"""evexml app unittests for views

"""
import json

from django.conf import settings
from django.test import TestCase
from django.shortcuts import reverse


class AddAPIViewTest(TestCase):
    """Tests for the view which displays the "Add API" form.

    """
    @classmethod
    def setUpClass(cls):
        super(AddAPIViewTest, cls).setUpClass()
        data_dir = getattr(settings, 'DATA_DIR')
        with data_dir.joinpath('conf', 'test_secrets.json').open() as handle:
            secrets = json.load(handle)
            cls.testkeys = secrets['apikeys']
        cls.url = reverse('eveapi_add')

    def test_invalid_api(self):
        """Ensure an invalid api is rejected.

        """
        response = self.client.post(self.url, data={
            'key_id': '1',
            'v_code': 'test'}, follow=True)
        self.assertContains(response, 'problem')

    # Mask: 4294967295
    def test_api_full_all(self):
        """Ensure full and account-wide keypair is accepted.

        """
        keypair = self.testkeys['full']['all']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'success')

    def test_api_full_char_corp(self):
        """Ensure full but corp character only keypair is rejected.

        """
        keypair = self.testkeys['full']['char_corp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')

    def test_api_full_char_noncorp(self):
        """Ensure full but non-corp character only keypair is rejected.

        """
        keypair = self.testkeys['full']['char_noncorp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')

    # Mask: 4294901631
    def test_api_partial_all(self):
        """Ensure partial and account-wide keypair is rejected.

        """
        keypair = self.testkeys['partial']['all']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')

    def test_api_partial_char_corp(self):
        """Ensure partial and corp character only keypair is rejected.

        """
        keypair = self.testkeys['partial']['char_corp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')

    def test_api_partial_char_noncorp(self):
        """Ensure partial and non-corp character only keypair is rejected.

        """
        keypair = self.testkeys['partial']['char_noncorp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')

    # Mask: 0
    def test_api_blank_all(self):
        """Ensure blank and account-wide keypair is rejected.

        """
        keypair = self.testkeys['blank']['all']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')

    def test_api_blank_char_corp(self):
        """Ensure blank and corp character only keypair is rejected.

        """
        keypair = self.testkeys['blank']['char_corp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')

    def test_api_blank_char_noncorp(self):
        """Ensure full but non-corp character only keypair is rejected.

        """
        keypair = self.testkeys['blank']['char_noncorp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')

    # Expires
    def test_api_expires_all(self):
        """Ensure full and account-wide but expiring keypair is rejected.

        """
        keypair = self.testkeys['full_expires']['all']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')

    def test_api_expires_char_corp(self):
        """Ensure full but corp character only, expiring keypair is rejected.

        """
        keypair = self.testkeys['full_expires']['char_corp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')

    def test_api_expires_char_noncorp(self):
        """Ensure full but non-corp character, expiring keypair is rejected.

        """
        keypair = self.testkeys['full_expires']['char_noncorp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
