"""evexml app unittests for views

"""
import json

from django.conf import settings
from django.test import TestCase
from django.shortcuts import reverse

from evexml.models import APIKeyPair


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

    def test_view_renders(self):
        """The view should render correctly.

        """
        self.client.get(self.url)

    def test_invalid_api(self):
        """Invalid api is rejected and not saved.

        """
        response = self.client.post(self.url, data={
            'key_id': '1',
            'v_code': 'test'}, follow=True)
        self.assertContains(response, 'problem')

    # Mask: 4294967295
    def test_valid_api(self):
        """Full and account-wide keypair is accepted and saved.

        """
        keypair = self.testkeys['full']['all']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'success')
