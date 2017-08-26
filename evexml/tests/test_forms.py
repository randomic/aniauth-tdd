import json

from django.test import TestCase
from django.conf import settings

from evexml.forms import AddAPIForm


class AddAPIFormTest(TestCase):
    """Tests for the view which displays the "Add API" form.

    """
    @classmethod
    def setUpClass(cls):
        super(AddAPIFormTest, cls).setUpClass()
        data_dir = getattr(settings, 'DATA_DIR')
        with data_dir.joinpath('conf', 'test_secrets.json').open() as handle:
            secrets = json.load(handle)
            cls.testkeys = secrets['apikeys']

    def test_invalid_api(self):
        """Ensure an invalid api is rejected.

        """
        form = AddAPIForm({
            'keyID': '1',
            'vCode': 'test'})
        self.assertFalse(form.is_valid())

    # Mask: 4294967295
    def test_api_full_all(self):
        """Ensure full and account-wide keypair is valid.

        """
        keypair = self.testkeys['full']['all']
        form = AddAPIForm({
            'keyID': keypair['keyID'],
            'vCode': keypair['vCode']})
        self.assertTrue(form.is_valid())

    def test_api_full_char_corp(self):
        """Ensure full but corp character only keypair is invalid.

        """
        keypair = self.testkeys['full']['char_corp']
        form = AddAPIForm({
            'keyID': keypair['keyID'],
            'vCode': keypair['vCode']})
        self.assertFalse(form.is_valid())

    def test_api_full_char_noncorp(self):
        """Ensure full but non-corp character only keypair is invalid.

        """
        keypair = self.testkeys['full']['char_noncorp']
        form = AddAPIForm({
            'keyID': keypair['keyID'],
            'vCode': keypair['vCode']})
        self.assertFalse(form.is_valid())
