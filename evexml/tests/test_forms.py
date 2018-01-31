from django.test import TestCase, mock
from evelink.api import APIError

from evexml.forms import AddAPIForm
from evexml.models import APIKeyPair

from .util import TEST_RESULTS


@mock.patch('evelink.account.Account.key_info')
class AddAPIFormTest(TestCase):
    """Tests for the view which displays the "Add API" form.

    """
    _key_id = '1234567890'
    _vcode = 'AddAPIFormTest'

    def count_keys_in_database(self):
        return APIKeyPair.objects.filter(key_id=self._key_id).count()

    def form(self):
        return AddAPIForm({'key_id': self._key_id, 'v_code': self._vcode})

    def test_invalid_api(self, mock_api):
        """Ensure an invalid api is rejected.

        """
        mock_api.side_effect = APIError(203, 'Authentication failure.')
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 0)

    # Mask: 4294967295
    def test_api_full_all(self, mock_api):
        """Ensure full and account-wide keypair is valid.

        """
        mock_api.return_value = TEST_RESULTS['full']['all']
        self.assertTrue(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    def test_api_full_char_corp(self, mock_api):
        """Ensure full but corp character only keypair is invalid.

        """
        mock_api.return_value = TEST_RESULTS['full']['char_corp']
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    def test_api_full_char_noncorp(self, mock_api):
        """Ensure full but non-corp character only keypair is invalid.

        """
        mock_api.return_value = TEST_RESULTS['full']['char_noncorp']
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    # Mask: 4294901631
    def test_api_partial_all(self, mock_api):
        """Partial and account-wide keypair is rejected but saved.

        """
        mock_api.return_value = TEST_RESULTS['partial']['all']
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    def test_api_partial_char_corp(self, mock_api):
        """Partial and corp character only keypair is rejected but saved.

        """
        mock_api.return_value = TEST_RESULTS['partial']['char_corp']
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    def test_api_partial_char_noncorp(self, mock_api):
        """Partial and non-corp character only keypair is rejected but saved.

        """
        mock_api.return_value = TEST_RESULTS['partial']['char_noncorp']
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    # Mask: 0
    def test_api_blank_all(self, mock_api):
        """Blank and account-wide keypair is rejected but saved.

        """
        mock_api.return_value = TEST_RESULTS['blank']['all']
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    def test_api_blank_char_corp(self, mock_api):
        """Blank and corp character only keypair is rejected but saved.

        """
        mock_api.return_value = TEST_RESULTS['blank']['char_corp']
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    def test_api_blank_char_noncorp(self, mock_api):
        """Full but non-corp character only keypair is rejected but saved.

        """
        mock_api.return_value = TEST_RESULTS['blank']['char_noncorp']
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    # Expires
    def test_api_expires_all(self, mock_api):
        """Full and account-wide but expiring keypair is rejected but saved.

        """
        mock_api.return_value = TEST_RESULTS['full_expires']['all']
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    def test_api_expires_char_corp(self, mock_api):
        """Full but corp character only expiring keypair is rejected but saved

        """
        mock_api.return_value = TEST_RESULTS['full_expires']['char_corp']
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    def test_api_expires_char_noncorp(self, mock_api):
        """Full but non-corp character expiring keypair is rejected but saved.

        """
        mock_api.return_value = TEST_RESULTS['full_expires']['char_noncorp']
        self.assertFalse(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)

    def test_duplicate_api(self, mock_api):
        """A duplicate should not be saved but should not display an error.

        """
        mock_api.return_value = TEST_RESULTS['full']['all']
        self.form().is_valid()
        self.assertTrue(self.form().is_valid())
        self.assertEqual(self.count_keys_in_database(), 1)
