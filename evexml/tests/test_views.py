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
