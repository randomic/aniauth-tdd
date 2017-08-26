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
        self.client.get(self.url)

    def test_invalid_api(self):
        """Invalid api is rejected and not saved.

        """
        response = self.client.post(self.url, data={
            'key_id': '1',
            'v_code': 'test'}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(APIKeyPair.objects.filter(key_id=1).count(), 0)

    # Mask: 4294967295
    def test_api_full_all(self):
        """Full and account-wide keypair is accepted and saved.

        """
        keypair = self.testkeys['full']['all']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'success')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)

    def test_api_full_char_corp(self):
        """Full but corp character only keypair is rejected but saved.

        """
        keypair = self.testkeys['full']['char_corp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)

    def test_api_full_char_noncorp(self):
        """Full but non-corp character only keypair is rejected but saved

        """
        keypair = self.testkeys['full']['char_noncorp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)

    # Mask: 4294901631
    def test_api_partial_all(self):
        """Partial and account-wide keypair is rejected but saved.

        """
        keypair = self.testkeys['partial']['all']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)

    def test_api_partial_char_corp(self):
        """Partial and corp character only keypair is rejected but saved.

        """
        keypair = self.testkeys['partial']['char_corp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)

    def test_api_partial_char_noncorp(self):
        """Partial and non-corp character only keypair is rejected but saved.

        """
        keypair = self.testkeys['partial']['char_noncorp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)

    # Mask: 0
    def test_api_blank_all(self):
        """Blank and account-wide keypair is rejected but saved.

        """
        keypair = self.testkeys['blank']['all']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)

    def test_api_blank_char_corp(self):
        """Blank and corp character only keypair is rejected but saved.

        """
        keypair = self.testkeys['blank']['char_corp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)

    def test_api_blank_char_noncorp(self):
        """Full but non-corp character only keypair is rejected but saved.

        """
        keypair = self.testkeys['blank']['char_noncorp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)

    # Expires
    def test_api_expires_all(self):
        """Full and account-wide but expiring keypair is rejected but saved.

        """
        keypair = self.testkeys['full_expires']['all']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)
    def test_api_expires_char_corp(self):
        """Full but corp character only expiring keypair is rejected but saved

        """
        keypair = self.testkeys['full_expires']['char_corp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)

    def test_api_expires_char_noncorp(self):
        """Full but non-corp character expiring keypair is rejected but saved.

        """
        keypair = self.testkeys['full_expires']['char_noncorp']
        response = self.client.post(self.url, data={
            'key_id': keypair['key_id'],
            'v_code': keypair['v_code']}, follow=True)
        self.assertContains(response, 'problem')
        self.assertEqual(
            APIKeyPair.objects.filter(key_id=keypair['key_id']).count(), 1)
