from django import forms
from django.forms.fields import IntegerField, CharField

import evelink.account


class AddAPIForm(forms.Form):
    key_id = IntegerField()
    v_code = CharField(max_length=64, min_length=1)

    def clean(self):
        self._clean()
        return super(AddAPIForm, self).clean()

    def _clean(self):
        """Check the access mask and characters of the supplied keypair.

        """
        key_id = self.cleaned_data.get('key_id')
        v_code = self.cleaned_data.get('v_code')
        if not (key_id and v_code):
            return

        api = evelink.api.API(api_key=(key_id, v_code))
        account = evelink.account.Account(api)
        try:
            key_info = account.key_info().result
        except evelink.api.APIError as error:
            self.add_error(None, error.message)
            return

        if key_info['type'] != 'account':
            self.add_error(None, 'The API key should select Character: All')
        if key_info['access_mask'] != 4294967295:
            self.add_error(None, 'The API key should have full access')
        if key_info['expire_ts']:
            self.add_error(None, 'The API key should have no expiry checked')
