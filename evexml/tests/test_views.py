"""evexml app unittests for views

"""
from django.test import TestCase, mock
from django.shortcuts import reverse
from evelink.api import APIError

from .util import TEST_RESULTS


@mock.patch('evelink.account.Account.key_info')
class AddAPIViewTest(TestCase):
    """Tests for the view which displays the "Add API" form.

    """
    _key_id = '1234567890'
    _vcode = 'AddAPIViewTest'
    _url = reverse('eveapi_add')

    def post_api_keypair(self):
        data = {'key_id': self._key_id, 'v_code': self._vcode}
        return self.client.post(self._url, data, follow=True)

    def test_view_renders(self, unused_mock):
        """The view should render correctly.

        """
        self.client.get(self._url)

    def test_invalid_api(self, mock_api):
        """Invalid api is rejected.

        """
        mock_api.side_effect = APIError(203, 'Authentication failure.')
        response = self.post_api_keypair()
        self.assertContains(response, 'API Error:')

    def test_correct_api(self, mock_api):
        """Full and account-wide keypair is accepted.

        """
        mock_api.return_value = TEST_RESULTS['full']['all']
        response = self.post_api_keypair()
        self.assertContains(response, 'successfully saved')

    def test_incorrect_api(self, mock_api):
        """Partial and account-wide keypair is rejected.

        """
        mock_api.return_value = TEST_RESULTS['partial']['all']
        response = self.post_api_keypair()
        self.assertContains(response, 'The API key should have full access')
